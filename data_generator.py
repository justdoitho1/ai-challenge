import random
import csv
import numpy as np
import math
batch_size = 70000
member_type = {
  1: '싱글',
  2: '4인가족',
  3: '대가족'
}
# user_list[0][0] = age
# user_list[0][1] = member_type
product_name = {
  0: [ '식기세척기 1', 0xFFFFFF],
  1: [ '식기세척기 2', 0xFF0000],
  2: [ '식기세척기 3', 0x00FF00],
  3: [ '식기세척기 4', 0x0000FF],
  4: [ '식기세척기 5', 0xF0F0F0],
  5: [ '식기세척기 6', 0xFF00F0],
  6: [ '식기세척기 7', 0xFF00F0],
  7: [ '식기세척기 8', 0xFFFFFF],
  8: [ '식기세척기 9', 0xF0F0F0],
  9: ['식기세척기 10', 0x00FF0F],
}
product_list = [
  ['렌탈비용', '용량', '만족도', '할인율', '제품코드'],
  [
    [23, 4, 0, 10, 0],
    [21, 3, 0, 5, 1],
  ],
  [
    [42, 8, 0, 10, 2],
    [38, 6, 0, 8, 3],
    [47, 10, 0, 10, 4],
    [43, 8, 0, 12, 5],
    [40, 10, 0, 5, 6],
  ],
  [
    [55, 16, 0, 8, 7],
    [58, 14, 0, 7, 8],
    [62, 18, 0, 8, 9],
  ]
]
user_list = [[0] * 7 for _ in range(batch_size)]
# Generate random user data
with open('user_data.csv', 'a', newline='', encoding='UTF8') as csvfile:
  csvfile.truncate(0)  # Clear the file if it exists
  csv_writer = csv.writer(csvfile)
    
  for i in range(0, batch_size):
    user_list[i][0] = random.randint(23, 70)  # age
    
    family = random.randint(1, 3)  # member type
    
    if family == 1:
      user_list[i][1] = random.randint(1, 3)
    elif family == 2:
      user_list[i][1] = random.randint(4, 5)
    else:
      user_list[i][1] = random.randint(7, 10)
      
    user_list[i][2:] = random.choice(product_list[family])
    user_list[i][4] = min(100,math.floor(np.random.normal(83, 7, 1)[0]))
    csv_writer.writerow(user_list[i])
  
csvfile.close()

