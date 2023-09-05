# -*- coding: utf-8 -*-

import os
import cv2
import numpy as np
import argparse
import warnings
import time

from src.anti_spoof_predict import AntiSpoofPredict
from src.generate_patches import CropImage
from src.utility import parse_model_name
warnings.filterwarnings('ignore')


CAMINHO_IMAGEM_EXEMPLO = "./images/sample/"

# Verifica se a imagem tem a proporção correta (4:3)
def verificar_imagem(imagem):
    altura, largura, canal = imagem.shape
    if largura/altura != 3/4:
        print("A imagem não está adequada!\nA altura/largura deve ser 4/3.")
        return False
    else:
        return True


def teste(imagem, diretorio_modelo, id_dispositivo):
    modelo_teste = AntiSpoofPredict(id_dispositivo)
    cortador_imagem = CropImage()
    # imagem = cv2.imread(CAMINHO_IMAGEM_EXEMPLO + nome_imagem)
    imagem = cv2.resize(imagem, (int(imagem.shape[0] * 3 / 4), imagem.shape[0]))
    resultado = verificar_imagem(imagem)
    if resultado is False:
        return
    imagem_bbox = modelo_teste.get_bbox(imagem)
    previsao = np.zeros((1, 3))
    velocidade_teste = 0
    # soma as previsões dos resultados de cada modelo individual
    for nome_modelo in os.listdir(diretorio_modelo):
        h_entrada, w_entrada, tipo_modelo, escala = parse_model_name(nome_modelo)
        parametro = {
            "org_img": imagem,
            "bbox": imagem_bbox,
            "scale": escala,
            "out_w": w_entrada,
            "out_h": h_entrada,
            "crop": True,
        }
        if escala is None:
            parametro["crop"] = False
        img = cortador_imagem.crop(**parametro)
        inicio = time.time()
        previsao += modelo_teste.predict(img, os.path.join(diretorio_modelo, nome_modelo))
        velocidade_teste += time.time()-inicio

    # desenha o resultado da previsão
    label = np.argmax(previsao)
    valor = previsao[0][label]/2

    return label


if __name__ == "__main__":
    desc = "test"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        "--id_dispositivo",
        type=int,
        default=0,
        help="qual id da GPU, [0/1/2/3]")
    parser.add_argument(
        "--model_dir",
        type=str,
        default="./resources/anti_spoof_models",
        help="modelo_lib usado para teste")
    parser.add_argument(
        "--nome_imagem",
        type=str,
        default="image_F1.jpg",
        help="imagem usada para teste")
    args = parser.parse_args()
    teste(args.nome_imagem, args.diretorio_modelo, args.id_dispositivo)
