
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftMASMENOSleftPORDIVIDIDODIVIDIDO ID MAS MENOS PARDER PARIZQ POR s\t: e e\t: e MAS t \n            | e MENOS t  e : t t\t: t POR f \n            | t DIVIDIDO f  t : f f\t: ID  f\t: PARIZQ e PARDER '
    
_lr_action_items = {'ID':([0,6,7,8,9,10,],[5,5,5,5,5,5,]),'PARIZQ':([0,6,7,8,9,10,],[6,6,6,6,6,6,]),'$end':([1,2,3,4,5,12,13,14,15,16,],[0,-1,-4,-7,-8,-2,-3,-5,-6,-9,]),'MAS':([2,3,4,5,11,12,13,14,15,16,],[7,-4,-7,-8,7,-2,-3,-5,-6,-9,]),'MENOS':([2,3,4,5,11,12,13,14,15,16,],[8,-4,-7,-8,8,-2,-3,-5,-6,-9,]),'PARDER':([3,4,5,11,12,13,14,15,16,],[-4,-7,-8,16,-2,-3,-5,-6,-9,]),'POR':([3,4,5,12,13,14,15,16,],[9,-7,-8,9,9,-5,-6,-9,]),'DIVIDIDO':([3,4,5,12,13,14,15,16,],[10,-7,-8,10,10,-5,-6,-9,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'s':([0,],[1,]),'e':([0,6,],[2,11,]),'t':([0,6,7,8,],[3,3,12,13,]),'f':([0,6,7,8,9,10,],[4,4,4,4,14,15,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> s","S'",1,None,None,None),
  ('s -> e','s',1,'p_S','gramatica2.py',78),
  ('e -> e MAS t','e',3,'p_E','gramatica2.py',82),
  ('e -> e MENOS t','e',3,'p_E','gramatica2.py',83),
  ('e -> t','e',1,'p_et','gramatica2.py',96),
  ('t -> t POR f','t',3,'p_T','gramatica2.py',100),
  ('t -> t DIVIDIDO f','t',3,'p_T','gramatica2.py',101),
  ('t -> f','t',1,'p_tf','gramatica2.py',114),
  ('f -> ID','f',1,'p_F_ID','gramatica2.py',119),
  ('f -> PARIZQ e PARDER','f',3,'p_F_PAR','gramatica2.py',124),
]