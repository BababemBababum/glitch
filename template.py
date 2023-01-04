from assets import generic_template_assets

elements = []
for i in range(len(generic_template_assets)):
    element = {
        'title': generic_template_assets[i]['title'],
        'buttons': [
            {
                'type': 'postback',
                'title': generic_template_assets[i]['buttons'][0]['First'],
                'payload':"USER_DEFINED_PAYLOAD"
            },
            {
                'type': 'postback',
                'title': generic_template_assets[i]['buttons'][0]['Second'],
                'payload':"USER_DEFINED_PAYLOAD"
            },
            {
                'type': 'postback',
                'title': generic_template_assets[i]['buttons'][0]['Third'],
                'payload':"USER_DEFINED_PAYLOAD"
            },
        ],
        'image_url': generic_template_assets[i]['image_url']
    }
    elements.append(element)
