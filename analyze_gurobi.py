import json
import pandas as pd


def gurobi_string_to_result(fpath):
  name = fpath.split("/")[-1].replace('.mps', '').replace('.gz', '').replace('.json', '')
  with open(fpath, 'r') as f:
    content = json.load(f)
    info = content['SolutionInfo']
    res_primal = 0
    res_dual = 0
    sol_time = float(info['Runtime'])
    status = info['Status']
    ipm_num = info.get("BarIterCount", 0)
    iter_num = info.get("IterCount", 0)
    
    if status != 3:
      val_primal = float(info['ObjVal'])
      val_dual = float(info['ObjVal'])
      sol_status = 'OPTIMAL' if status == 2 else "UNFINISHED"
    else:
      sol_status = "INFEASIBLE"
      val_primal = -1e6
      val_dual = -1e6

    return dict(res_primal=res_primal.__round__(8),
                res_dual=res_dual.__round__(8),
                sol_time=sol_time.__round__(4),
                val_primal=val_primal.__round__(4),
                val_dual=val_dual.__round__(4),
                sol_status=sol_status,
                ipm_num=ipm_num,
                iteration_num=iter_num,
                name=name)


if __name__ == '__main__':
  import sys
  result = gurobi_string_to_result(
    "../miplib2017-bench/grb_sol/pre_wachplan.json")
  print(result)

