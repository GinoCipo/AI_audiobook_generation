import extractor
import tts
import audiobook

if __name__ == "__main__":
    content, paper_name = extractor.miner()

    spk_id = tts.get_speaker()

    request_ids = []
    for paragraph in content:
        request_ids.append(tts.request_conversion(spk_id, paragraph))

    audios = []
    for id in request_ids:
        audios.append(tts.fetch_conversion(id))

    paper = audiobook.build_audio(audios, paper_name)
    print(f"Your paper has been saved as {paper}.")