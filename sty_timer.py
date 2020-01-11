# A little study timer.
# Mode:
# 1. Default: <Free Mode>: only record total study time, don't have a time limit.
# 2. countdown: <CountDown Mode>, with timelimit,

import sys
import time
import tqdm
import argparse

def end_study(sty_time):
    hours = sty_time // 3600
    mins = (sty_time % 3600) // 60
    print('\nTotal Sty time:', hours, 'hours,', mins, 'mins.\a')
    
    try:
        flag = input('Enough for today? (y/yes/^c).........').lower()
    except KeyboardInterrupt:
        print('\nEnjoy the rest of your day.')
        sys.exit(0)
    
    if flag in ['y', 'yes']:
        print('Enjoy the rest of your day.')
        sys.exit(0)
    
    try:
        _ = input('Take a break, Press Any Button to resume...')
    except KeyboardInterrupt:
        print('\nEnjoy the rest of your day.')
        sys.exit(0)  
    

def terminate(sty_time):
    hours = sty_time // 3600
    mins = (sty_time % 3600) // 60
    print('Total Sty time:', hours, 'hours,', mins, 'mins.\a')
    sys.exit(0)
    
class Timer(tqdm.tqdm):
    @property
    def format_dict(self):
        d = super(Timer, self).format_dict
        total_time = d["n"]
        left_time = d["total"] - d["n"]
        d.update(total_time=self.format_interval(total_time))
        d.update(left_time=self.format_interval(left_time))

        return d

def start_sty(mode='free', total_time=60*60*24):
    print('\nStart forcusing...\a')

    hours = 0
    mins = 0
    secs = 0

    if mode == 'free':
        dis_format = '[Total Study Time : {total_time}]'
    else:
        dis_format = '{bar}| [Total Study Time : {total_time}; Remaining time : {left_time}]'

    for sty_time in Timer(range(total_time), bar_format=dis_format):
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            end_study(sty_time)

    terminate(total_time)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='A Study timer')

    # Use <Countdown mode>.
    parser.add_argument('-c', '--countdown', help='countdown mode, unit is in minute', type=int)
    
    args = parser.parse_args()

    if args.countdown is None:
        print('<Free> Mode.')
        start_sty()
    else:
        print('<CountDown> Mode, total sty time:', args.countdown, 'minutes.')
        start_sty(mode='c', total_time=args.countdown*60)
