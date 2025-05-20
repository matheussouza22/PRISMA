from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


def webscrapping_supervia(url, origin, destin, model, line):
    """
    Extrai e formata os horários de transporte do site Moovit.

    Args:
        url (str): URL da página com a tabela de horários
        origin (str): Local de origem
        destin (str): Local de destino
        model (str): Modal (ex: Trem, Ônibus)
        line (str): Nome ou código da linha

    Returns:
        pd.DataFrame: DataFrame formatado com os horários
    """
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        print("Acessando o site...")
        driver.get(url)

        print("Aguardando carregamento da tabela...")
        wait = WebDriverWait(driver, 10)
        table_wrapper = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "table-wrapper")))

        titulo = driver.find_element(By.CLASS_NAME, "table-title").text
        print(f"Extraindo dados da tabela: {titulo}")

        dias = []
        header_cells = driver.find_elements(By.XPATH, "//thead//th")
        for cell in header_cells:
            dias.append(cell.text)

        horarios = {dia: [] for dia in dias}
        linhas = driver.find_elements(By.XPATH, "//tbody//tr")

        for linha in linhas:
            celulas = linha.find_elements(By.TAG_NAME, "td")
            if len(celulas) == len(dias):
                for i, celula in enumerate(celulas):
                    horario = celula.text.strip()
                    if horario:
                        horarios[dias[i]].append(horario)

        df = pd.DataFrame(horarios)

    except Exception as e:
        print(f"Ocorreu um erro durante a extração: {e}")
        df = pd.DataFrame()
    finally:
        driver.quit()
        print("Navegador fechado.")

    if df.empty:
        return pd.DataFrame(columns=["MODAL", "LINHA_COD", "LINHA_DESCRICAO", "DESTINO", "DIA", "HORA", "ORIGEM"])

    df["Origem"] = origin
    df["Destino"] = destin
    df["Modal"] = model

    df_melted = df.melt(
        id_vars=["Origem", "Modal", "Destino"],
        var_name="DIA_TIPO",
        value_name="HORA"
    )

    # Expandir "Dias úteis" em SEG, TER, QUA, QUI, SEX
    dias_uteis = ["SEG", "TER", "QUA", "QUI", "SEX"]
    df_expandido = pd.DataFrame()

    for _, row in df_melted.iterrows():
        if row["DIA_TIPO"] == "Dias úteis":
            for dia in dias_uteis:
                nova_linha = row.copy()
                nova_linha["DIA"] = dia
                df_expandido = pd.concat([df_expandido, pd.DataFrame([nova_linha])], ignore_index=True)
        elif row["DIA_TIPO"] == "sábado":
            row["DIA"] = "SAB"
            df_expandido = pd.concat([df_expandido, pd.DataFrame([row])], ignore_index=True)
        elif row["DIA_TIPO"] == "domingo":
            row["DIA"] = "DOM"
            df_expandido = pd.concat([df_expandido, pd.DataFrame([row])], ignore_index=True)

    df_expandido["MODAL"] = df_expandido["Modal"]
    df_expandido["LINHA_COD"] = line
    df_expandido["LINHA_DESCRICAO"] = df_expandido["Origem"] + " - " + df_expandido["Destino"]
    df_expandido["DESTINO"] = df_expandido["Destino"]
    df_expandido["ORIGEM"] = df_expandido["Origem"]

    df_final = df_expandido[["MODAL", "LINHA_COD", "LINHA_DESCRICAO", "DESTINO", "DIA", "HORA", "ORIGEM"]]
    df_final_limpo = df_final[df_final["HORA"] != "-"].reset_index(drop=True)

    return df_final_limpo


def webscrapping_supervia_tres_tabela(url, origin, destin, model, line):
    """
    Extrai e formata os horários de transporte do site Moovit.

    Args:
        url (str): URL da página com a tabela de horários
        origin (str): Local de origem
        destin (str): Local de destino
        model (str): Modal (ex: Trem, Ônibus)
        line (str): Nome ou código da linha

    Returns:
        pd.DataFrame: DataFrame formatado com os horários
    """

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        print("Acessando o site...")
        driver.get(url)

        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "table-title")))

        titulos = driver.find_elements(By.CLASS_NAME, "table-title")
        tabelas = driver.find_elements(By.CLASS_NAME, "table-wrapper")

        df_dias_uteis = pd.DataFrame()
        df_sabado = pd.DataFrame()
        df_domingo = pd.DataFrame()

        for titulo, tabela in zip(titulos, tabelas):
            dia = titulo.text.strip().lower()

            headers = tabela.find_elements(By.XPATH, ".//thead//th")
            colunas = [h.text.strip() for h in headers]

            linhas = tabela.find_elements(By.XPATH, ".//tbody//tr")
            dados = []
            for linha in linhas:
                celulas = linha.find_elements(By.TAG_NAME, "td")
                dados.append([c.text.strip() for c in celulas])

            df_temp = pd.DataFrame(dados, columns=colunas)
            df_temp["DIA"] = titulo.text.strip()
            df_temp["ORIGEM"] = origin
            df_temp["DESTINO"] = destin
            df_temp["MODAL"] = model
            df_temp["LINHA_DESCRICAO"] = origin + " - " + destin
            df_temp["LINHA_COD"] = line


            if "dias úteis" in dia:
                df_dias_uteis = df_temp
            elif "sábado" in dia:
                df_sabado = df_temp
            elif "domingo" in dia:
                df_domingo = df_temp

        print("Extração finalizada com sucesso.")

    except Exception as e:
        print("Erro na extração:", e)

    finally:
        driver.quit()


    dias_uteis = ["SEG", "TER", "QUA", "QUI", "SEX"]
    colunas = ["MODAL", "LINHA_COD", "LINHA_DESCRICAO", "DESTINO", "DIA", "HORA", "ORIGEM"]

    dados_lista = []

    # === DIAS ÚTEIS ===
    for _, row in df_dias_uteis.iterrows():
        for dia in dias_uteis:
            dados_lista.append({
                "MODAL": row["MODAL"],
                "LINHA_COD": row["LINHA_COD"],
                "LINHA_DESCRICAO": row["LINHA_DESCRICAO"],
                "DESTINO": row["DESTINO"],
                "DIA": dia,
                "HORA": row["Central Do Brasil"],
                "ORIGEM": row["ORIGEM"]
            })

    # === SÁBADO ===
    colunas_partidas = [
        col for col in df_sabado.columns
        if col not in ['Estação', 'DIA', 'ORIGEM', 'DESTINO', 'MODAL', 'LINHA_DESCRICAO', 'LINHA_COD']
    ]

    horarios_sabado = df_sabado.loc[0, colunas_partidas].tolist()
    horarios_sabado = [hora for hora in horarios_sabado if pd.notna(hora) and hora != "-"]
    linha_sabado = df_sabado.loc[0]

    for hora in horarios_sabado:
        dados_lista.append({
            "MODAL": linha_sabado["MODAL"],
            "LINHA_COD": linha_sabado["LINHA_COD"],
            "LINHA_DESCRICAO": linha_sabado["LINHA_DESCRICAO"],
            "DESTINO": linha_sabado["DESTINO"],
            "DIA": "SAB",
            "HORA": hora,
            "ORIGEM": linha_sabado["ORIGEM"]
        })

    # === DOMINGO ===

    colunas_partidas = [
        col for col in df_domingo.columns
        if col not in ['Estação', 'DIA', 'ORIGEM', 'DESTINO', 'MODAL', 'LINHA_DESCRICAO', 'LINHA_COD']
    ]
    horarios_domingo = df_domingo.loc[0, colunas_partidas].tolist()
    horarios_domingo = [hora for hora in horarios_domingo if pd.notna(hora) and hora != "-"]
    linha_domingo = df_domingo.loc[0]

    for hora in horarios_domingo:
        dados_lista.append({
            "MODAL": linha_domingo["MODAL"],
            "LINHA_COD": linha_sabado["LINHA_COD"],
            "LINHA_DESCRICAO": linha_domingo["LINHA_DESCRICAO"],
            "DESTINO": linha_domingo["DESTINO"],
            "DIA": "DOM",
            "HORA": hora,
            "ORIGEM": linha_domingo["ORIGEM"]
        })

    # === Criar DataFrame final ===
    dados_completos = pd.DataFrame(dados_lista, columns=colunas)
    
    
    return dados_completos




def webscrapping_supervia_dias_uteis(url, origin, destin, model, line):
    """
    Extrai e formata os horários de transporte do site Moovit quando possuir apenas uma tabela de dias úteis.

    Args:
        url (str): URL da página com a tabela de horários
        origin (str): Local de origem
        destin (str): Local de destino
        model (str): Modal (ex: Trem, Ônibus)
        line (str): Nome ou código da linha

    Returns:
        pd.DataFrame: DataFrame formatado com os horários
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        print("Acessando o site...")
        driver.get(url)

        print("Aguardando carregamento da tabela...")
        wait = WebDriverWait(driver, 10)
        table_wrapper = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "table-wrapper")))

        titulo = driver.find_element(By.CLASS_NAME, "table-title").text
        print(f"Extraindo dados da tabela: {titulo}")

        dias = []
        header_cells = driver.find_elements(By.XPATH, "//thead//th")
        for cell in header_cells:
            dias.append(cell.text)

        horarios = {dia: [] for dia in dias}
        linhas = driver.find_elements(By.XPATH, "//tbody//tr")

        for linha in linhas:
            celulas = linha.find_elements(By.TAG_NAME, "td")
            if len(celulas) == len(dias):
                for i, celula in enumerate(celulas):
                    horario = celula.text.strip()
                    if horario:
                        horarios[dias[i]].append(horario)

        df = pd.DataFrame(horarios)

    except Exception as e:
        print(f"Ocorreu um erro durante a extração: {e}")
        return pd.DataFrame()
    finally:
        driver.quit()
        print("Navegador fechado.")

    dados_lista = []

    dias_uteis = ["SEG", "TER", "QUA", "QUI", "SEX"]

    colunas_partidas = [
        col for col in df.columns
        if col not in ['Estação']
    ]

    horarios_dias_uteis = df.loc[0, colunas_partidas].tolist()


    for hora in horarios_dias_uteis:
        for dia in dias_uteis:
            dados_lista.append({
                "MODAL": model,
                "LINHA_COD": line,
                "LINHA_DESCRICAO": origin + "-" + destin,
                "DESTINO": destin,
                "DIA": dia,
                "HORA": hora,
                "ORIGEM": origin
            })


    df_formatado = pd.DataFrame(dados_lista)


    return df_formatado




def webscrapping_tabela_apenas_finais_de_semana(url, origin, destin, model, line):
    """
    Extrai e formata os horários de transporte do site Moovit quando possuir apenas uma tabela de dias úteis.

    Args:
        url (str): URL da página com a tabela de horários
        origin (str): Local de origem
        destin (str): Local de destino
        model (str): Modal (ex: Trem, Ônibus)
        line (str): Nome ou código da linha

    Returns:
        pd.DataFrame: DataFrame formatado com os horários
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        print("Acessando o site...")
        driver.get(url)

        print("Aguardando carregamento da tabela...")
        wait = WebDriverWait(driver, 10)
        table_wrapper = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "table-wrapper")))

        titulo = driver.find_element(By.CLASS_NAME, "table-title").text
        print(f"Extraindo dados da tabela: {titulo}")

        dias = []
        header_cells = driver.find_elements(By.XPATH, "//thead//th")
        for cell in header_cells:
            dias.append(cell.text)

        horarios = {dia: [] for dia in dias}
        linhas = driver.find_elements(By.XPATH, "//tbody//tr")

        for linha in linhas:
            celulas = linha.find_elements(By.TAG_NAME, "td")
            if len(celulas) == len(dias):
                for i, celula in enumerate(celulas):
                    horario = celula.text.strip()
                    if horario:
                        horarios[dias[i]].append(horario)

        df = pd.DataFrame(horarios)

    except Exception as e:
        print(f"Ocorreu um erro durante a extração: {e}")
        return pd.DataFrame()
    finally:
        driver.quit()
        print("Navegador fechado.")

    dados_lista = []

    dias_uteis = ["SAB", "DOM"]

    colunas_partidas = [
        col for col in df.columns
        if col not in ['Estação']
    ]

    horarios_dias_uteis = df.loc[0, colunas_partidas].tolist()

    for hora in horarios_dias_uteis:
        for dia in dias_uteis:
            dados_lista.append({
                "MODAL": model,
                "LINHA_COD": line,
                "LINHA_DESCRICAO": origin + "-" + destin,
                "DESTINO": destin,
                "DIA": dia,
                "HORA": hora,
                "ORIGEM": origin
            })


    df_formatado = pd.DataFrame(dados_lista)


    return df_formatado
