## A study Timer

#### Usage:
- User Guide: ```python study_timer -[h|help]```.

- Mode:
    - **Free Mode \{default\}**: ```python study_timer```
        - Without time constraint. (Though there's a upper limit of 24 hours).

    - **CountDown Mode**        : ```python study_timer -{c|countdown} {Time}```
        - Total study time will be set to {Time} minutes, and end the study when time is up.

- General Cmd:
    - Press ```Ctrl-c``` or ```^c``` to pause if you want to have a short break.
    - Under Pausing mode, could use ```^c``` or ```{q|quit}<CR>``` to end study; ```<CR>``` to continue.
