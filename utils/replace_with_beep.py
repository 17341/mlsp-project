import logging
from pydub.generators import Sine

def replace_with_beep(audio, start_time, end_time, beep_frequency=1000):
    """
    Replace a specific time interval in an audio segment with a beep sound.

    Args:
        audio (AudioSegment): The input audio segment.
        start_time (int): Start time (in milliseconds) of the interval to be replaced.
        end_time (int): End time (in milliseconds) of the interval to be replaced.
        beep_frequency (int): Frequency (in Hz) of the beep sound.

    Returns:
        AudioSegment: The output audio segment with the specified interval replaced by a beep.
    """
    logger = logging.getLogger(__name__)

    if start_time > end_time:
        logger.error("Start time can't be greater than end time.")
        return None

    try:
        before_interval = audio[:start_time]
        beep = Sine(beep_frequency).to_audio_segment(duration= end_time - start_time)
        after_interval = audio[end_time:]

        output_audio = before_interval + beep + after_interval

        return output_audio
    except IndexError as e:
        logger.error(f"IndexError: {e}")
        return None
    except ValueError as e:
        logger.error(f"ValueError: {e}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        logger.exception(e)
        return None