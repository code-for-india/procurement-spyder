proc.find({proc_id: 'OP00021008'})
proj.find({id : 'P130339'})
proj.find({id : 'P130339'}).select({sector: 1})
proc.remove({proc_id: 'OP00021008'})
