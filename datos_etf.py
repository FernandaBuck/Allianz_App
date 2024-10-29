
etfs = [
    {
        "nombre": "QQQ NASDAQ 100",
        "descripcion": "ETF que sigue el rendimiento del índice NASDAQ 100.",
        "simbolo": "QQQ"
    },
    {
        "nombre": "SPDR S&P 500 ETF TRUST",
        "descripcion": "ETF que sigue el rendimiento del índice S&P 500.",
        "simbolo": "SPY"
    },
    {
        "nombre": "SPDR DJIA TRUST",
        "descripcion": "ETF que sigue el rendimiento del índice Dow Jones Industrial Average.",
        "simbolo": "DIA"
    },
    {
        "nombre": "VANGUARD EMERGING MARKET ETF",
        "descripcion": "ETF de Vanguard que sigue el rendimiento de mercados emergentes.",
        "simbolo": "VWO"
    },
    {
        "nombre": "FINANCIAL SELECT SECTOR SPDR",
        "descripcion": "ETF que sigue el rendimiento del sector financiero de EE.UU.",
        "simbolo": "XLF"
    },
    {
        "nombre": "HEALTH CARE SELECT SECTOR",
        "descripcion": "ETF que sigue el rendimiento del sector de salud de EE.UU.",
        "simbolo": "XLV"
    },
    {
        "nombre": "DJ US HOME CONSTRUCT",
        "descripcion": "ETF que sigue el rendimiento del sector de construcción de viviendas en EE.UU.",
        "simbolo": "ITB"
    },
    {
        "nombre": "SILVER TRUST",
        "descripcion": "ETF que sigue el precio de la plata.",
        "simbolo": "SLV"
    },
    {
        "nombre": "MSCI TAIWAN INDEX FD",
        "descripcion": "ETF que sigue el rendimiento del índice MSCI Taiwan.",
        "simbolo": "EWT"
    },
    {
        "nombre": "MSCI UNITED KINGDOM",
        "descripcion": "ETF que sigue el rendimiento del índice MSCI United Kingdom.",
        "simbolo": "EWU"
    },
    {
        "nombre": "MSCI SOUTH KOREA IND",
        "descripcion": "ETF que sigue el rendimiento del índice MSCI South Korea.",
        "simbolo": "EWY"
    },
    {
        "nombre": "MSCI EMU",
        "descripcion": "ETF que sigue el rendimiento del índice MSCI EMU (Unión Monetaria Europea).",
        "simbolo": "EZU"
    },
    {
        "nombre": "MSCI JAPAN INDEX FD",
        "descripcion": "ETF que sigue el rendimiento del índice MSCI Japan.",
        "simbolo": "EWJ"
    },
    {
        "nombre": "MSCI CANADA",
        "descripcion": "ETF que sigue el rendimiento del índice MSCI Canada.",
        "simbolo": "EWC"
    },
    {
        "nombre": "MSCI GERMANY INDEX",
        "descripcion": "ETF que sigue el rendimiento del índice MSCI Germany.",
        "simbolo": "EWG"
    },
    {
        "nombre": "MSCI AUSTRALIA INDEX",
        "descripcion": "ETF que sigue el rendimiento del índice MSCI Australia.",
        "simbolo": "EWA"
    },
    {
        "nombre": "BARCLAYS AGGREGATE",
        "descripcion": "ETF que sigue el rendimiento del índice de bonos Barclays Aggregate.",
        "simbolo": "AGG"
    }
]

# Ejemplo para mostrar los datos
for etf in etfs:
    print(f"Nombre: {etf['nombre']}, Símbolo: {etf['simbolo']}, Descripción: {etf['descripcion']}")
