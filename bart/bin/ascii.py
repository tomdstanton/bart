#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from random import choice
def bart_ascii():
    bart = f'''
              ,  ,
             / \/ \,'| _
            ,'    '  ,' |,|
           ,'           ' |,'|
          ,'                 ;'| _
         ,'                    '' |
        ,'                        ;-,
       (___                        /
     ,'    `.  ___               ,'
    :       ,`'   `-.           /
    |-._ o /         \         /
   (    `-(           )       /
  ,'`.     \      o  /      ,'
 /    `     `.     ,'      /
(             `"""'       /
 `._                     /
    `--.______        '"`.
       \__,__,`---._   '`;
            ))`-^--')`,-'
          ,',_____,'  |
          \_          `).
           `.      _,'  `
            /`-._,-'      \
'''+choice(["eat my shorts!", "don't have a cow, man!", "i didn't do it.", "ay caramba!"])
    return bart