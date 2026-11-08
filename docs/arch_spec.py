W, H = 1400, 690
TITLE = 'Pipeline de queimadas · Medallion'
SUBTITLE = 'INPE + IBGE → Bronze → Silver → Gold, com reprocessamento em Databricks'

GROUPS = [
    dict(style='plain', x=30, y=100, w=180, h=290, label='Fontes públicas'),
    dict(style='plain', x=260, y=90, w=770, h=310, label='Pipeline local · Python'),
    dict(style='plain', x=290, y=130, w=180, h=240, label='Bronze', dash='',
         colors=dict(stroke='#A0522D', fill='#FBF1EA', text='#8B4513')),
    dict(style='plain', x=550, y=130, w=180, h=240, label='Silver', dash='',
         colors=dict(stroke='#8A939B', fill='#F4F6F7', text='#5D6770')),
    dict(style='plain', x=810, y=130, w=190, h=240, label='Gold', dash='',
         colors=dict(stroke='#C9A227', fill='#FFF9E6', text='#9A7B0A')),
    dict(style='plain', x=260, y=440, w=770, h=220, label='Databricks Free Edition · Unity Catalog', dash='',
         colors=dict(stroke='#FF3621', fill='#FFF5F3', text='#C42A18')),
]

NODES = [
    dict(icon='inpe', x=120, y=180, label=['INPE', 'focos mensais']),
    dict(icon='ibge', x=120, y=310, size=48, label=['IBGE', 'Censo 2022']),
    dict(icon='apacheparquet', x=380, y=230, label=['Parquet', 'cópia fiel + linhagem'], chips=['python']),
    dict(icon='apacheparquet', x=640, y=230, label=['Parquet', 'filtro AQUA_M-T · join'], chips=['pandas']),
    dict(icon='apacheparquet', x=905, y=230, label=['Parquet', 'indicadores · clusters'], chips=['pandas', 'scikitlearn']),
    dict(icon='Users', x=1280, y=230, label=['Órgãos ambientais', 'dashboard · relatório']),
    dict(icon='databricks', x=380, y=560, size=52, label=['Volume', 'Parquets da Bronze']),
    dict(icon='apachespark', x=640, y=560, label=['PySpark', 'Silver + Gold']),
    dict(icon='deltalake', x=905, y=560, size=52, label=['Delta Lake', 'silver_focos · gold_municipios']),
]

EDGES = [
    dict(points=[(152, 180), (240, 180), (240, 215), (348, 215)], label='CSV', label_at=(196, 180)),
    dict(points=[(148, 310), (240, 310), (240, 245), (348, 245)], label='API', label_at=(196, 310)),
    dict(points=[(412, 230), (608, 230)], label='silver.py', label_at=(510, 230)),
    dict(points=[(672, 230), (873, 230)], label='gold.py', label_at=(770, 230)),
    dict(points=[(937, 230), (1248, 230)], label='análises', label_at=(1110, 230)),
    dict(points=[(380, 350), (380, 530)], label='upload', label_at=(380, 418)),
    dict(points=[(410, 560), (608, 560)], label='spark.read', label_at=(510, 560)),
    dict(points=[(672, 560), (875, 560)], label='saveAsTable', label_at=(770, 560)),
]
