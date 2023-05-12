library(ggplot2)
library(dplyr)

# Clean graph data 
graphs <- read.csv("small_graphs.csv")
df <- read.csv("small_results.csv")

df <- df[c("graph_name", "alg_name", "time", "number_of_colors")]
write.csv(df, "small_results_trimmed.csv", row.names = FALSE)

# Transform random graph data

