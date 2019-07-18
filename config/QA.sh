#!/bin/bash
echo "Please Select:
帮助：通过编辑修改QA0.txt到QA3.txt执行不同的组合脚本，可以自行修改txt达到目的。
注意：目前测试mac系统通过，其他系统请自行调试。
请选择对应数字：
1.QUANTAXIS >QA1.txt(save all:save stock_day/xdxr/ index_day/ stock_list/index_list)
2.QUANTAXIS >QA2.txt(save day:save stock_day/xdxr index_day etf_day stock_list/index_list)
3.QUANTAXIS >QA3.txt(save financialfiles 保存高级财务数据(自1996年开始))
0.QUANTAXIS >QA0.txt(save stock_block:保存板块 & save stock_info:保存tushare数据接口获取的股票列表)"
read -p "Enter selection [0-3] >" num

if [[ $num =~ ^[0-3]$ ]]; then
   if [[ $num == 0 ]]; then
     echo "QUANTAXIS >QA0.txt"
    quantaxis < QA0.txt 
	exit;
   fi

  if [[ $num == 1 ]]; then
    echo "QUANTAXIS >QA1.txt"
    quantaxis < QA1.txt
    exit
  fi

  if [[ $num == 2 ]]; then
	echo "QUANTAXIS >QA2.txt"
    quantaxis < QA2.txt
    exit;
  fi

  if [[ $num == 3 ]]; then
    echo "QUANTAXIS >QA3.txt"
    quantaxis < QA3.txt
    exit;
  fi
else
 echo "Invalid entry." >&2
 exit 1
fi
