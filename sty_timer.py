# A little study timer.
# Mode:
# 1. Default: <Free Mode>: only record total study time, don't have a time limit.
# 2. countdown: <CountDown Mode>, with timelimit,

import sys
import time
import tqdm
import argparse

def end_study(sty_time, terminated: bool) -> None:
    '''
    "Pause" Function, judge whether user want to (quit or take a break).
    Params:
     - sty_time: Cumulated study time.
     - terminated: (bool), use to indicate whether reaches the time limit.
    '''

    hours = sty_time // 3600
    mins = (sty_time % 3600) // 60
    print('\nTotal Sty time:', hours, 'hours,', mins, 'mins.\a')
    
    if not terminated:
        try:
            flag = input('Pausing, Use (quit/q/^c) to end study; Press Any Button to resume.........').lower()
        except KeyboardInterrupt:
            print('\nEnjoy the rest of your day.')
            sys.exit(0)
        
        if flag in ['q', 'quit']:
            print('Enjoy the rest of your day.')
            sys.exit(0)
    
    
class Timer(tqdm.tqdm):
    '''
    Define Timer and output format.
    '''
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
    terminate_flag = False

    if mode == 'free':
        dis_format = '[Total Study Time : {total_time}]'
    else:
        dis_format = '[Total Study Time : {total_time}; Remaining time : {left_time}| {bar}]'

    for sty_time in Timer(range(total_time), bar_format=dis_format):
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            end_study(sty_time, terminate_flag)
    
    terminate_flag = True
    end_study(total_time, terminate_flag)


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
