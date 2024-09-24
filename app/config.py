import os
from dotenv import load_dotenv
load_dotenv()

token = os.getenv("TOKEN")
#categorias/ML3530
#tipos/free
#tipos/gold_special
#cotizaciones/uyu
#cotizaciones/eur
#dolares/mep
#dolares/blue

endpoints= {
    "/categorias/{valor}":{"url":"https://api.mercadolibre.com/categories/{}",
                           "header": {
                           'Authorization': f'Bearer {token}'
                            }
        },
    "/tipos/{valor}":{"url":"https://api.mercadolibre.com/sites/MLA/listing_types/{}",
                           "header": {
                           'Authorization': f'Bearer {token}'
                            }
        },
    "/cotizaciones/{valor}":{"url":"https://dolarapi.com/v1/cotizaciones/{}",
                           "header": {}
        },
    "/dolares/{valor}":{"url":"https://dolarapi.com/v1/dolares/{}",
                           "header": {}
        },
    
    
    }

reglas={
    "ip":[{
            "method": "GET",
            "limite": 15,
            "cantidad":0,
            "tiempo":100,
            "tiempo_de_espera":130,
            "tiempo_ultima_request":None,
            "ip" : "127.0.0.1",


    
     },{
            "method": "GET",
            "limite": 10,
            "cantidad":0,
            "tiempo":120,
            "tiempo_de_espera":130,
            "tiempo_ultima_request":None,
            "ip" : "192.168.1.36",


    
 }
    ],
"path":[{
            "method": "GET",
            "limite": 11,
            "cantidad":0,
            "tiempo":60,
            "tiempo_de_espera":90,
            "tiempo_ultima_request":None,
            "path" : "/dolares/",
            "regex":r".*"

    
    },
        {
            "method": "GET",
            "limite": 8,
            "cantidad":0,
            "tiempo":60,
            "tiempo_de_espera":90,
            "tiempo_ultima_request":None,
            "path" : "/tipos/",
            "regex":r".*"

    
    }
    ],

"ip_path":[ 
        {
            "method": "GET",
            "limite": 2,
            "cantidad":0,
            "tiempo":200,
            "tiempo_de_espera":90,
            "tiempo_ultima_request":None,
            "path":'/cotizaciones/',
            "regex":r".*",
            "ip" : "192.168.1.36",
        
    
        },
    
        {
            "method": "GET",
            "limite": 5,
            "cantidad":0,
            "tiempo":100,
            "tiempo_de_espera":120,
            "tiempo_ultima_request":None,
            "path":"/categorias/",
            "regex":r".*",
            "ip" : "127.0.0.1",
    
    },

        
]
    
}

lista_de_ips_permitidas= [reglas["ip"],reglas["ip_path"]]
lista_de_ips_permitidas = {item["ip"]for sublista in lista_de_ips_permitidas for item in sublista}

