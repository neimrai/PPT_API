{  
  "name": "示例演示文稿",  
  "slides": [  
    {  
      "background": {  
        "color": "ffffff",  
        "opacity": 1.0  
      },  
      "note": "这是第一张幻灯片的演讲者备注",  
      "shapes": [  
        {  
          "shape_type": "textbox",  
          "position": {  
            "left": 100,  
            "top": 50,  
            "width": 600,  
            "height": 80  
          },  
          "fill": {  
            "color": "f0f0f0",  
            "opacity": 0.8  
          },  
          "text_wrap": true,  
          "paragraphs": [  
            {  
              "text": "欢迎使用演示文稿",  
              "font": {  
                "name": "Inter",  
                "size": 24,  
                "font_weight": 700,  
                "italic": false,  
                "color": "333333"  
              },  
              "alignment": 1  
            }  
          ]  
        },  
        {  
          "shape_type": "autoshape",  
          "type": 1,  
          "position": {  
            "left": 200,  
            "top": 200,  
            "width": 400,  
            "height": 100  
          },  
          "fill": {  
            "color": "4285f4",  
            "opacity": 1.0  
          },  
          "stroke": {  
            "color": "1a73e8",  
            "thickness": 2.0,  
            "opacity": 1.0  
          },  
          "shadow": {  
            "radius": 4,  
            "offset": 2,  
            "color": "000000",  
            "opacity": 0.3,  
            "angle": 45  
          },  
          "border_radius": 8,  
          "text_wrap": true,  
          "paragraphs": [  
            {  
              "text": "这是一个带样式的文本框",  
              "font": {  
                "name": "Inter",  
                "size": 16,  
                "font_weight": 400,  
                "italic": false,  
                "color": "ffffff"  
              },  
              "alignment": 2  
            }  
          ]  
        },  
        {  
          "shape_type": "picture",  
          "position": {  
            "left": 50,  
            "top": 350,  
            "width": 200,  
            "height": 150  
          },  
          "clip": true,  
          "opacity": 1.0,  
          "invert": false,  
          "border_radius": [10, 10, 10, 10],  
          "shape": "RECTANGLE",  
          "object_fit": {  
            "fit": "COVER",  
            "focus": [0.5, 0.5]  
          },  
          "picture": {  
            "is_network": true,  
            "path": "https://example.com/image.jpg"  
          }  
        },  
        {  
          "shape_type": "connector",  
          "type": 1,  
          "position": {  
            "left": 300,  
            "top": 400,  
            "width": 200,  
            "height": 2  
          },  
          "thickness": 1.5,  
          "color": "666666",  
          "opacity": 1.0  
        }  
      ]  
    }  
  ]  
}