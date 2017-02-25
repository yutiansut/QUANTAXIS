library("rJava")
library("RMongo")
mongo <- mongoDbConnect("stock", "localhost", 27017)
output <- dbGetQuery(mongo, "ts",'')