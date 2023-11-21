from pydub import AudioSegment
import logging


def rearrange_chunks(chunks):
    logging.info("Starting to rearrange chunks")

    # Check if chunks list is empty
    if not chunks:
        logging.error("No chunks provided to rearrange")
        return None

    try:
        sorted_chunks = sorted(chunks, key=lambda x: x['start_time'])
        combined_segment = AudioSegment.silent(duration=0)

        for segment in sorted_chunks:
            start_time = segment['start_time']
            end_time = segment['end_time']
            audio = segment['audio_segment']

            if start_time > len(audio) or end_time > len(audio):
                logging.warning(
                    f"Start or end time exceeds audio length for segment {segment}")
                continue

            sliced_audio = audio[start_time:end_time]
            combined_segment += sliced_audio

        logging.info("Successfully rearranged chunks")
        return combined_segment

    except Exception as e:
        logging.error(f"An error occurred while rearranging chunks: {e}")
        return None
