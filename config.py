
reglas={
    "ip":[{
            "method": "GET",
            "limite": 10,
            "cantidad":0,
            "tiempo":100,
            "tiempo_de_espera":130,
            "tiempo_ultima_request":None,
            "ips" : ["127.0.0.1"],
            "path":"/",

    
     },{
            "method": "GET",
            "limite": 12,
            "cantidad":0,
            "tiempo":120,
            "tiempo_de_espera":130,
            "tiempo_ultima_request":None,
            "ips" : ["192.168.1.36"],
            "path":"/",

    
 }
    ],
"path":[{
            "method": "GET",
            "limite": 5,
            "cantidad":0,
            "tiempo":60,
            "tiempo_de_espera":90,
            "tiempo_ultima_request":None,
            "path" : "/dolar_blue/",
            "regex":"*",

    
    },
        {
            "method": "GET",
            "limite": 10,
            "cantidad":0,
            "tiempo":60,
            "tiempo_de_espera":90,
            "tiempo_ultima_request":None,
            "path" : "/feriados/",
            "regex":"*",

    
    }
    ],

"ip_path":{
    
    
                "validaciones":[
                    {
                        "method": "GET",
                        "limite": 10,
                        "cantidad":0,
                        "tiempo":200,
                        "tiempo_de_espera":90,
                        "tiempo_ultima_request":None,
                        "path":'/cotizaciones/',
                        "regex":"*",
                        "ips" : ["192.168.1.36"],
                    
                
                 },
                
                    {
                        "method": "GET",
                        "limite": 4,
                        "cantidad":0,
                        "tiempo":100,
                        "tiempo_de_espera":120,
                        "tiempo_ultima_request":None,
                        "path":"/feriados/",
                        "regex":"*",
                        "ips" : ["192.168.1.40"],
                
            },

        ]
 }
    
    
    
}
