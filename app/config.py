
reglas={
    "ip":[{
            "method": "GET",
            "limite": 19,
            "cantidad":0,
            "tiempo":100,
            "tiempo_de_espera":130,
            "tiempo_ultima_request":None,
            "ips" : ["127.0.0.1"],
            "path":"/",

    
     },{
            "method": "GET",
            "limite": 18,
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
            "limite": 15,
            "cantidad":0,
            "tiempo":60,
            "tiempo_de_espera":90,
            "tiempo_ultima_request":None,
            "path" : "/dolar_blue/",
            "regex":"*",

    
    },
        {
            "method": "GET",
            "limite": 8,
            "cantidad":0,
            "tiempo":60,
            "tiempo_de_espera":90,
            "tiempo_ultima_request":None,
            "path" : "/tipos/",
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
                        "ips" : ["192.168.1.39"],
                    
                
                 },
                
                    {
                        "method": "GET",
                        "limite": 5,
                        "cantidad":0,
                        "tiempo":100,
                        "tiempo_de_espera":120,
                        "tiempo_ultima_request":None,
                        "path":"/categorias/",
                        "regex":"*",
                        "ips" : ["192.168.1.36"],
                
            },

        ]
 }
    
    
    
}
