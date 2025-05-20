import requests
import pandas as pd
import time

def coletar_paradas_niteroi(salvar_csv=True, caminho_csv="paradas_niteroi_ida_volta.csv"):
    """
    Coleta as paradas (latitude, longitude e endereço) de todas as linhas de ônibus de Niterói (RJ),
    para ambos os sentidos (ida e volta), e salva em um arquivo CSV se desejado.

    Args:
        salvar_csv (bool): Se True, salva os dados em um arquivo CSV.
        caminho_csv (str): Caminho do arquivo CSV a ser salvo.

    Returns:
        pd.DataFrame: DataFrame com colunas: linha, latitude, longitude, endereco, direcao.
    """

    def obter_paradas(numero_linha, shape_id):
        url = "https://mobnit.niteroi.rj.gov.br/api/website/v1/conteudo/dados/area-publica/itinerarios/paradas"
        params = {
            "from": 1740787200000,
            "to": 1743465599999,
            "numeroLinha": f"'{numero_linha}'",
            "shapeId": f"'{shape_id}'"
        }
        headers = {
            "User-Agent": "ConsultaTransporteNiteroiBot"
        }
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erro ao consultar linha {numero_linha} ({shape_id}): {response.status_code}")
            return []

    original_dict = {
        "15": "51535_I", "21": "51520_I", "22": "51534_I", "22A": "2759389_I", "24": "51645_I",
        "26": "51609_I", "26A": "51617_I", "28": "62560_I", "30": "75279_I", "31": "51376_I",
        "32": "25329_I", "33": "25330_I", "34A": "35599_I", "34B": "35600_I", "35": "37737_I",
        "36": "35601_I", "37": "36133_I", "38A": "37735_I", "39A": "35602_I", "40": "25825_I",
        "41BC": "58711_I", "41JB": "58717_I", "42S": "81553_I", "42T": "58802_I", "43.2": "74013_I",
        "44": "35603_I", "45": "35604_I", "46": "37694_I", "47": "75280_I", "47A": "75282_I",
        "47B": "75281_I", "48": "37712_I", "48B": "37746_I", "48SP": "78269_I", "49.1": "51334_I",
        "49.2": "51358_I", "52": "37738_I", "52A": "37741_I", "53": "35605_I", "54": "35606_I",
        "55A": "37752_I", "57": "58679_I", "60": "51570_I", "61": "58807_I", "62": "50962_I",
        "66C": "79904_I", "67": "58707_I", "OC1": "35624_I", "OC2": "36831_I", "OC3": "58591_I",
        "OC3A": "37742_I"
    }

    converted_dict = {
        linha: [sid, sid.replace("_I", "_V")] if sid.endswith("_I") else [sid]
        for linha, sid in original_dict.items()
    }

    dados = []
    for linha, shape_list in converted_dict.items():
        for shape_id in shape_list:
            time.sleep(0.3)  # Evita sobrecarregar o servidor
            direcao = shape_id.split("_")[-1]  # "I" ou "V"
            paradas = obter_paradas(linha, shape_id)
            for p in paradas:
                dados.append({
                    "linha": linha,
                    "latitude": p["latitude"],
                    "longitude": p["longitude"],
                    "endereco": p["parada"],
                    "direcao": direcao
                })

    df = pd.DataFrame(dados)

    if salvar_csv:
        df.to_csv(caminho_csv, index=False)
        print(f"[✔] Arquivo salvo com sucesso: {caminho_csv}")

    return df

if __name__ == "__main__":
    # Executa a coleta e salva por padrão em CSV
    coletar_paradas_niteroi()
