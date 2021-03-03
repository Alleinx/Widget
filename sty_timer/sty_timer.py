# A little study timer.
# Mode:
# 1. Default: <Free Mode>: only record total study time, don't have a time limit.
# 2. countdown: <CountDown Mode>, with time limit,

import sys
import time
import tqdm
import argparse

def get_time_str() -> str:
    local_time = time.localtime()
    time_str = time.strftime('-> [%m-%d, %H:%M:%S]', local_time)

    return time_str

def end_study(terminated: bool) -> None:
    '''
    "Pause" Function, judge whether the user want to (end study or take a break).

    Params:
     - terminated: (bool), use to indicate whether reaches the time limit.
    '''

    # Change lines here:
    print('')

    if not terminated:
        start_break_time = get_time_str()

        try:
            flag = input(
                '\n{} Pausing, Use (quit/q/^c) to end study; Press Any Button to resume.........'.format(start_break_time)).lower()
        except KeyboardInterrupt:
            print('\n\nEnjoy the rest of your day.')
            sys.exit(0)

        if flag in ['q', 'quit']:
            print('\nEnjoy the rest of your day.')
            sys.exit(0)

        # get the time when user end the break:
        end_break_time = get_time_str()
        print('\n{} Back to work.'.format(end_break_time))

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
    time_str = get_time_str()

    print('\n{} Start focusing...'.format(time_str))
    terminate_flag = False

    if mode == 'free':
        dis_format = '[Total Study Time : {total_time}]'
    else:
        dis_format = '[Total Study Time : {total_time}; Remaining time : {left_time}| {bar}]'

    for _ in Timer(range(total_time), bar_format=dis_format):
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            end_study(terminate_flag)

    terminate_flag = True
    end_study(terminate_flag)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A Study timer')

    # Use <Countdown mode>.
    parser.add_argument(
        '-c',
        '--countdown',
        help='countdown mode, unit is in minute',
        type=int)

    args = parser.parse_args()

    if args.countdown is None:
        print('<Free> Mode.')
        start_sty()
    else:
        print('<CountDown> Mode, total sty time:', args.countdown, 'minutes.')
        start_sty(mode='c', total_time=args.countdown*60)
