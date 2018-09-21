# coding: utf8

import os, glob, json, sys, argparse, ConfigParser, datetime, smtplib
import RPi.GPIO as GPIO
from time import sleep
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

def send_mail (relay_message):
# config.get("Defaults", "relay_pin")
    msg = MIMEMultipart()
    msg['From'] = config.get("Mail", "msg_from")
    msg['To'] = config.get("Mail", "msg_to")
    msg['Subject'] = config.get("Mail", "msg_subject")
    message = relay_message
    msg.attach(MIMEText(message))

    mailserver = smtplib.SMTP(config.get("Mail", "mailserver"),int(config.get("Mail", "smtp_port")))
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.ehlo()
    mailserver.login(config.get("Mail", "mail_login"), config.get("Mail", "mail_pass"))
    mailserver.sendmail(config.get("Mail", "from"),config.get("Mail", "to_email"),msg.as_string())
    mailserver.quit()

def createParser ():
    parser = argparse.ArgumentParser(
        prog = 'kotel',
        description = '''The remote thermal boiler control system''',
        epilog = '''(c) AndrDI 2018. Without any responsibility''')
    parser.add_argument ('--config', '-c', required=True, metavar = 'CONFIG_FILE')
    return parser

def read_current_interval (interval):
    from distutils.util import strtobool
    t_now = now_time
    t_start = datetime.datetime.strptime(interval['time_start'], "%H:%M")
    t_end   = datetime.datetime.strptime(interval['time_end'], "%H:%M")

    t_start = t_now.replace(hour=t_start.hour, minute=t_start.minute, second=0)
    t_end   = t_now.replace(hour=t_end.hour, minute=t_end.minute, second=0)

    stamp_now   = (t_now - datetime.datetime(1970, 1, 1)).total_seconds()
    stamp_start = (t_start - datetime.datetime(1970, 1, 1)).total_seconds()
    stamp_end   = (t_end - datetime.datetime(1970, 1, 1)).total_seconds()

    if stamp_start > stamp_end:
        if stamp_now < stamp_start:
            stamp_start = stamp_start - 86400
        else:
            stamp_end = stamp_end + 86400

    if ((stamp_start < stamp_now) and (stamp_now < stamp_end)):
        return True

def read_all_intervals ():
    relay_current = False
    for i in relay:
        if read_current_interval(i):
            relay_current =  True
    return relay_current

def read_temp_raw(device_file):
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw(device_file)
    lines2 = read_temp_raw(device_file2)

    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw(device_file)
    equals_pos = lines[1].find('t=')

    while lines2[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines2 = read_temp_raw(device_file2)
    equals_pos2 = lines2[1].find('t=')

    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0

    if equals_pos2 != -1:
        temp_string = lines2[1][equals_pos2+2:]
        temp_c2 = float(temp_string) / 1000.0

    temp_status = "Current temperature 1: " + str(temp_c) + " \nCurrent temperature 2: " + str(temp_c2)

    return temp_status

if __name__ == '__main__':

    parser = createParser()
    namespace = parser.parse_args()
    config = ConfigParser.RawConfigParser()
    config.read(namespace.config)
    relay_pin = int(config.get("Relay", "relay_pin"))
    sleep_time = int(config.get("Defaults", "sleep_time"))
    relay = json.loads(config.get("Relay", "intervals"))
    base_dir = '/sys/bus/w1/devices/'

    device_folder = glob.glob(base_dir + '28*')[0]
    device_folder2 = glob.glob(base_dir + '28*')[1]
    device_file = device_folder + '/w1_slave'
    device_file2 = device_folder2 + '/w1_slave'

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(relay_pin, GPIO.OUT)
    state = GPIO.input(relay_pin)
    print "\nStarting kotel service\n" + str(read_temp())
    message = "Starting kotel service\n\n" + str(read_temp())
    if state == 0:
        print "Relay state is ON! Set it OFF and sleep 10 second"
        message = message + "Relay state is ON! Set it OFF and sleep 10 second\n"
        GPIO.output(relay_pin, GPIO.HIGH)
        sleep(sleep_time)
    relay_old = False
    send_mail(message)

    while True:
        message = ""
        now_time = datetime.datetime.now().replace(microsecond=0)
        relay_now = read_all_intervals ()
        if (relay_now != relay_old):
            if relay_now:
                message = message + str(now_time) + " Relay ON\n"
                print now_time, " Relay ON"
                GPIO.output(relay_pin, GPIO.LOW)
            else:
                message = message + str(now_time) + " Relay OFF\n"
                print now_time, " Relay OFF"
                GPIO.output(relay_pin, GPIO.HIGH)
            current_temp = (read_temp())
            print current_temp
            message = message + current_temp
            send_mail(message)
        relay_old = relay_now
        sleep(sleep_time)

GPIO.cleanup()
