WITH 'file:///health_data.csv' AS uri
LOAD CSV WITH HEADERS FROM uri AS row
CREATE (p:Patient {
  id:         toInteger(row.id),
  age:        toInteger(row.age),
  gender:     row.gender,
  height:     toInteger(row.height),
  weight:     toInteger(row.weight),
  ap_hi:      toInteger(row.ap_hi),
  ap_lo:      toInteger(row.ap_lo),
  cholesterol:toInteger(row.cholesterol),
  gluc:       toInteger(row.gluc),
  smoke:      toInteger(row.smoke),
  alco:       toInteger(row.alco),
  active:     toInteger(row.active),
  cardio:     toInteger(row.cardio)
})
RETURN p;
