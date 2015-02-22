SIMPLE_DATA = {
    "categories": [
        {
            "title": "Best Picture",
            "key": "best-picture",
            "nominees": [{
                "title": "Foo",
                "key": "foo",
                "image_url": "foo.jpg"
            }]
        }
    ],
    "points": {"best-picture": 10}
}


RAX_AUTH_DATA = {
    "access": {
        "token": {
            "expires": "2015-06-12T22:51:02.000-06:00",
            "id": "TOKEN"
        },
        "user": {
            "RAX-AUTH:defaultRegion": "ORD"
        },
        "serviceCatalog": [
            {
                "endpoints": [
                    {
                        "internalURL": "https://ord.queuest.com/v1",
                        "publicURL": "{{QUEUE_URL}}/v1",
                        "region": "ORD"
                    },
                    {
                        "internalURL": "https://dfw.queues.com/v1/111",
                        "publicURL": "https://dfw-int.queues.com/v1/111",
                        "region": "DFW"
                    }
                ],
                "name": "cloudQueues",
                "type": "rax:queues"
            }
        ]
    }
}
