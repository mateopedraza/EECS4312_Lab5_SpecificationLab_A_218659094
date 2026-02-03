## Student Name: Mateo Pedraza 
## Student ID: 218659094

"""
Stub file for the meeting slot suggestion exercise.

Implement the function `suggest_slots` to return a list of valid meeting start times
on a given day, taking into account working hours, and possible specific constraints. See the lab handout
for full requirements.
"""
from typing import List, Dict

def suggest_slots(
    events: List[Dict[str, str]],
    meeting_duration: int,
    day: str
) -> List[str]:
    """
    Suggest possible meeting start times for a given day.

    Args:
        events: List of dicts with keys {"start": "HH:MM", "end": "HH:MM"}
        meeting_duration: Desired meeting length in minutes
        day: Three-letter day abbreviation (e.g., "Mon", "Tue", ... "Fri")

    Returns:
        List of valid start times as "HH:MM" sorted ascending
    """
    if meeting_duration <= 0:
        return []

    WORK_START = 9 * 60   # 09:00
    WORK_END = 17 * 60    # 17:00
    LUNCH_START = 12 * 60 # 12:00
    LUNCH_END = 13 * 60   # 13:00
    SLOT_STEP = 15
    BUFFER_AFTER_EVENT = 15

    def parse_time(value: str) -> int:
        parts = value.split(":")
        if len(parts) != 2:
            raise ValueError("Invalid time format")
        hour = int(parts[0])
        minute = int(parts[1])
        if hour < 0 or hour > 23 or minute < 0 or minute > 59:
            raise ValueError("Invalid time value")
        return hour * 60 + minute

    def format_time(minutes: int) -> str:
        return f"{minutes // 60:02d}:{minutes % 60:02d}"

    blocked_events: List[tuple[int, int]] = []
    for event in events:
        try:
            start = parse_time(event.get("start", ""))
            end = parse_time(event.get("end", ""))
        except (ValueError, TypeError):
            continue
        if end <= start:
            continue
        if end <= WORK_START or start >= WORK_END:
            continue
        blocked_events.append((start, end + BUFFER_AFTER_EVENT))

    blocked_events.append((LUNCH_START, LUNCH_END))

    slots: List[str] = []
    latest_start = WORK_END - meeting_duration
    start = WORK_START
    while start <= latest_start:
        end = start + meeting_duration
        if end <= WORK_END:
            overlaps = False
            for b_start, b_end in blocked_events:
                if start < b_end and end > b_start:
                    overlaps = True
                    break
            if not overlaps:
                slots.append(format_time(start))
        start += SLOT_STEP

    return slots
