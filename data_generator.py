import random
import csv
batch_size = 20000
member_type = {
  1: '싱글',
  2: '4인가족',
  3: '대가족'
}
# user_list[0][0] = age
# user_list[0][1] = member_type
product_name = {
  1: '식기세척기 1',
  2: '식기세척기 2',
  3: '식기세척기 3',
  4: '식기세척기 4',
  5: '식기세척기 5',
  6: '식기세척기 6',
  7: '식기세척기 7',
  8: '식기세척기 8',
  9: '식기세척기 9',
  10: '식기세척기 10',
  11: '식기세척기 11',
  12: '식기세척기 12',
  13: '식기세척기 13',
  14: '식기세척기 14',
  15: '식기세척기 15',
  16: '식기세척기 16',
  17: '식기세척기 17',
  18: '식기세척기 18'
}
product_list = [
  ['렌탈비용', '용량', '만족도', '제품색깔', '할인율', '제품코드'],
  [
    [23000, 4, 0, 0xFFFFFF, 10, 1],
    [21000, 3, 0, 0xFF0000, 5, 2],
    [27000, 4, 0, 0x00FF00, 10, 3],
    [33000, 6, 0, 0x0000FF, 7, 4],
  ],
  [
    [42000, 8, 0, 0xF0F0F0, 10, 5],
    [45000, 10, 0, 0xFF00F0, 8, 6],
    [50000, 12, 0, 0xFFFFFF, 7, 7],
    [47000, 10, 0, 0xF0F0F0, 10, 8],
    [50000, 12, 0, 0x00FF0F, 8, 9],
    [43000, 8, 0, 0x000F0F, 12, 10],
    [40000, 10, 0, 0xF00F00, 5, 11],
    [38000, 6, 0, 0xFF00FF, 5, 12],
  ],
  [
    [45000, 12, 0, 0xF0F0F0, 10, 13],
    [55000, 16, 0, 0xFF00F0, 8, 14],
    [58000, 14, 0, 0xFFFFFF, 7, 15],
    [60000, 16, 0, 0xF0F0F0, 10, 16],
    [62000, 18, 0, 0x00FF0F, 8, 17],
    [57000, 14, 0, 0x000F0F, 10, 18],
  ]
]
user_list = [[0] * 8 for _ in range(batch_size)]
# Generate random user data
with open('user_data.csv', 'a', newline='') as csvfile:
  csvfile.truncate(0)  # Clear the file if it exists
  csv_writer = csv.writer(csvfile)
  csv_writer.writerow(['나이', '가족 구성원', '렌탈비용', '용량', '만족도', '제품색깔', '할인율', '제품코드'])  # Write header
    
  for i in range(0, batch_size):
    user_list[i][0] = random.randint(23, 70)  # age
    user_list[i][1] = random.randint(1, 3)  # member type
    
    user_list[i][2:] = random.choice(product_list[user_list[i][1]])
    user_list[i][4] = random.randint(25, 49) / 10
    csv_writer.writerow(user_list[i])
  
csvfile.close()

