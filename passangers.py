# -*- encoding: utf-8 -*-

def process(data, events, car):

  for event in events:

    if event["type"] == "switch":

      number_otstegnut = event["cars"]
      train_from = event["train_from"]
      train_to = event["train_to"]

      for poezd in data:
        if poezd["name"] == train_from:
          # если хотим отстегнуть слишком много
          if len(poezd["cars"]) < number_otstegnut:
            return -1
          # если всё хорошо, запомним что хотели отстегнуть и отстегнули вагоны
          else:
            otstegnuli = poezd["cars"][len(poezd["cars"])-number_otstegnut:]
            poezd["cars"] = poezd["cars"][:-number_otstegnut]

      for poezd in data:
        if poezd["name"] == train_to:
          poezd["cars"].extend(otstegnuli)
      

    elif event["type"] == "walk":
      
      walk_pass = event["passenger"]
      current_car = None
      dist = event["distance"]
      
      for poezd in data:
        for num_vagon in range(len(poezd["cars"])):
          # если пассажир в вагоне, запомним номер вагона и поезд и удалим пассажира
          if walk_pass in poezd["cars"][num_vagon]["people"]:
            
            current_car = num_vagon
            current_poezd = poezd["name"]
            poezd["cars"][num_vagon]["people"].remove(walk_pass)

      # если выбрали несуществующего пассажира
      if current_car is None:
        return -1
      # проверяем не пытается ли пассажир выйти из поезда
      if dist > 0:
        new_car = current_car + abs(dist)
      elif dist < 0:
        new_car = current_car - abs(dist)
        if new_car < 0:
          return -1
      
      for poezd in data:
        for num_vagon in range(len(poezd["cars"])):
          # если пассажир в верном вагоне и в верном поезде оставляем его в нём
          if num_vagon == new_car and poezd["name"] == current_poezd:
            poezd["cars"][num_vagon]["people"].append(walk_pass)
      
  for poezd in data:
    for vag in poezd["cars"]:
      if car in vag.values():
          return len(vag["people"])











