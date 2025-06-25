import random
import csv

batch_size = 100
member_type = {
  1: 'single',
  2: 'family',
  3: 'large_family'
}
# user_list[0][0] = index
# user_list[0][1] = age
# user_list[0][2] = member_type
product_name = {
  
}
product_list = [
  ['렌탈비용', '용량', '만족도', '제품색깔', '할인율', '제품코드'],
  [
    [],
    [],
    [],
    [],
  ],
  [
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
  ],
  [
    [],
    [],
    [],
    [],
    [],
    [],
  ]
]
user_list = [[0] * (2 + len(product_list[0])) for _ in range(batch_size)]
# Generate random user data
with open('user_data.csv', 'a', newline='') as csvfile:
  csvfile.truncate(0)  # Clear the file if it exists
  csv_writer = csv.writer(csvfile)
  csv_writer.writerow(['index', 'age', 'member_type'])  # Write header
    
  for i in range(0, batch_size):
    user_list[i][0] = random.randint(23, 70)  # age
    user_list[i][1] = random.randint(1, 3)  # member type
    
    user_list[i][2:] = random.choice(product_list[user_list[i][2]])
    csv_writer.writerow(user_list[i])
  
csvfile.close()

