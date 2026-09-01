import numpy as np
import tensorflow as tf  # type: ignore[import-not-found]
import tensorflow_hub as hub  # type: ignore[import-not-found]

YAMNET_URL = "https://tfhub.dev/google/yamnet/1"
DISTRESS_LABELS = {"Screaming", "Shout", "Yell", "Crying, sobbing", "Children shouting"}
THRESHOLD = 0.3

model = None
labels = None


def load_model():
    global model
    if model is None:
        model = hub.load(YAMNET_URL)
    return model


def load_labels(m):
    global labels
    if labels is not None:
        return labels
    path = m.class_map_path().numpy().decode("utf-8")
    labels = []
    with tf.io.gfile.GFile(path) as f:
        next(f)
        for line in f:
            labels.append(line.strip().split(",")[2])
    return labels


def check_distress(waveform, sample_rate=16000):
    if sample_rate != 16000:
        raise ValueError("expected 16kHz audio")

    m = load_model()
    class_names = load_labels(m)

    scores, embeddings, spec = m(waveform)
    avg_scores = np.mean(scores.numpy(), axis=0)

    top_idx = np.argmax(avg_scores)
    top_label = class_names[top_idx]
    top_conf = float(avg_scores[top_idx])

    is_distress = False
    for label in DISTRESS_LABELS:
        if label not in class_names:
            continue
        idx = class_names.index(label)
        if avg_scores[idx] > THRESHOLD:
            is_distress = True
            top_label = label
            top_conf = float(avg_scores[idx])
            break

    return {
        "is_distress": is_distress,
        "top_label": top_label,
        "confidence": round(top_conf, 3),
    }


if __name__ == "__main__":
    test_wave = np.zeros(16000, dtype=np.float32)
    print(check_distress(test_wave))