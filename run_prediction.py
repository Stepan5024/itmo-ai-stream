import argparse
import os
import yaml
import torch
import pandas as pd
from transformers import BertForSequenceClassification, BertTokenizer


def load_input_text(input_obj):
    """Загружает текст из файла или строки."""
    if isinstance(input_obj, str) and os.path.isfile(input_obj):
        if not input_obj.endswith(".txt"):
            raise ValueError("Invalid file type: only txt files supported.")
        with open(input_obj, encoding="utf-8") as f:
            text = f.read().splitlines()
    elif isinstance(input_obj, str):
        text = input_obj
    else:
        raise ValueError("Invalid input type: input type must be a string or a txt file.")
    return text

def run(config_path, checkpoint_path, input_obj, dest_file, device="cpu"):
    """Загружает модель и выполняет предсказания."""
    # Загрузите конфигурацию
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)["config"]

    # Инициализируйте модель и токенизатор
    model = BertForSequenceClassification.from_pretrained(
        config["arch"]["args"]["model_type"],
        num_labels=config["arch"]["args"]["num_classes"],
    )
    tokenizer = BertTokenizer.from_pretrained(config["arch"]["args"]["model_type"])

    # Загрузите веса из чекпоинта
    checkpoint = torch.load(checkpoint_path, map_location=device)
    
    # Удаляем префикс "model." из ключей
    new_state_dict = {k.replace("model.", ""): v for k, v in checkpoint["state_dict"].items()}
    
    # Загружаем state_dict в модель
    model.load_state_dict(new_state_dict, strict=False)
    
    model.to(device)
    model.eval()

    # Загрузите входные данные
    text = load_input_text(input_obj)

    # Токенизация и предсказание
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True).to(device)
    with torch.no_grad():
        outputs = model(**inputs)
        predictions = torch.sigmoid(outputs.logits).cpu().numpy()

    # Создайте DataFrame с результатами
    res_df = pd.DataFrame(
        predictions,
        columns=config["dataset"]["args"]["classes"],
        index=[text] if isinstance(text, str) else text,
    ).round(5)

    # Вывод в консоль
    print(res_df)

    # Сохранение в файл
    if dest_file is not None:
        res_df.index.name = "input_text"
        res_df.to_csv(dest_file, encoding="utf-8-sig")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="text, list of strings, or txt file",
    )
    parser.add_argument(
        "--config",
        type=str,
        default="hparams.yaml",
        help="path to config file (default: hparams.yaml)",
    )
    parser.add_argument(
        "--checkpoint",
        type=str,
        default="checkpoints/epoch=0-step=8511.ckpt",
        help="path to checkpoint file (default: checkpoints/epoch=0-step=8511.ckpt)",
    )
    parser.add_argument(
        "--save_to",
        type=str,
        default=None,
        help="destination path to output model results to (default: None)",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cpu",
        help="device to load the model on (default: cpu)",
    )

    args = parser.parse_args()

    run(
        config_path=args.config,
        checkpoint_path=args.checkpoint,
        input_obj=args.input,
        dest_file=args.save_to,
        device=args.device,
    )