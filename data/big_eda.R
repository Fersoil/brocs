library(ggplot2)
library(dplyr)
library(stringr)
library(forcats)
library(knitr)

# Load graph data
graphs <- read.csv("big_graphs.csv")
df <- read.csv("raw_big_results.csv")

# Combine data into a better structure
df <- df %>%
  mutate(
    graph_type = str_split_i(
      str_replace(graph_name, "dense_random", "dense-random"),
      "_",
      -4
    ),
    num_vertices = str_split_i(graph_name, "_", -3),
    num_edges = str_split_i(graph_name, "_", -2),
    graph_internal_id = strtoi(
      str_replace(
        str_split_i(graph_name, "_", -1),
        "g",
        ""
      )
    )
  ) %>%
  mutate(
    graph_id = graph_name,
    .keep = "unused"
  ) %>%
  mutate(
    time_ms = time / 100000 # Convert to ms
  ) %>%
  select(graph_id, graph_type, num_vertices, num_edges, alg_name, time_ms, number_of_colors, graph_internal_id)

deltas <- graphs %>%
  select(graph_name, big_delta) %>%
  mutate(graph_id = graph_name, .keep = "unused")
   
full_df <- df %>%
  left_join(deltas, by = "graph_id")
  
# Explore full_df

## Check row count
nrow(full_df) #Should be 150000 = 150 graphs x 500 tries x 2 algs

full_df %>%
  group_by(graph_id) %>%
  count()

## Save for use later
write.csv(full_df, file = "big_results.csv", row.names = FALSE)

## Explore random single_graph
deltas %>%
  filter(graph_id == "dense_random_100_1000_g1")

full_df %>%
  filter(graph_id == "dense_random_100_1000_g1") %>%
  filter(alg_name == "BrooksAlgorithm") %>%
  select(time_ms, number_of_colors) %>%
  summary()

full_df %>%
  filter(graph_id == "dense_random_100_1000_g1") %>%
  filter(alg_name == "ConnectedSequential") %>%
  select(time_ms, number_of_colors) %>%
  summary()

## Display size of the sizes
table(full_df$num_vertices)


## Display loaded graphs
graphs %>%
  mutate(
    graph_type = str_split_fixed(
      str_replace(graph_name, "dense_random", "dense-random"),
      "_",
      4
    )[, 1]
  ) %>%
  select(graph_type, num_of_vertices, num_of_edges, big_delta) %>%
  group_by(graph_type, num_of_vertices, num_of_edges) %>%
  summarise(
    average_big_delta = mean(big_delta)
  )

## Look collectivly on biggest graphs

### Mean time spent
full_df %>%
  filter(num_vertices == 500) %>%
  filter(num_edges == 5000) %>%
  filter(graph_type == "random") %>%
  mutate(
    graph_display_name = paste("Graph nr.", graph_internal_id)
  ) %>%
  group_by(graph_display_name, alg_name) %>%
  summarise(time_mean = mean(time_ms)) %>%
  ggplot(aes(x = graph_display_name, y = time_mean, fill = alg_name)) +
  geom_bar(position="dodge", stat="identity", alpha = 1) + 
  labs(
    title = "Mean time spent per algorithm",
    subtitle = "Run for 5 random graphs with 500 nodes and 5000 vertices",
    fill = "Name of the algorithm",
    x = "Name of the graph",
    y = "Mean time spent (in ms)"
  ) +
  scale_y_continuous(breaks = scales::pretty_breaks(n = 20))

### Time spent variance
full_df %>%
  filter(num_vertices == 500) %>%
  filter(num_edges == 5000) %>%
  filter(graph_type == "random") %>%
  mutate(
    graph_display_name = paste("Graph nr.", graph_internal_id)
  ) %>%
  group_by(graph_display_name, alg_name) %>%
  summarise(time_mean = var(time_ms)) %>%
  ggplot(aes(x = graph_display_name, y = time_mean, fill = alg_name)) +
  geom_bar(position="dodge", stat="identity", alpha = 1) + 
  labs(
    title = "Variance of the time spent per algorithm",
    subtitle = "Run for 5 random graphs with 500 nodes and 5000 vertices",
    fill = "Name of the algorithm",
    x = "Name of the graph",
    y = "Variance of the time spent (in ms^2)"
  ) + 
  scale_y_continuous(breaks = scales::pretty_breaks(n = 20))

### Time spent histogram
full_df %>%
  filter(num_vertices == 500) %>%
  filter(num_edges == 5000) %>%
  filter(graph_type == "random") %>%
  mutate(
    graph_display_name = paste("Graph nr.", graph_internal_id)
  ) %>%
  group_by(graph_display_name, alg_name) %>%
  ggplot(aes(time_ms, fill = alg_name)) + 
  geom_histogram() + 
  facet_wrap(~graph_display_name, nrow = 2) +
  labs(
    title = "Time spent per algorithm",
    subtitle = "Run for 5 random graphs with 500 nodes and 5000 vertices",
    fill = "Name of the algorithm",
    x = "Time spent (in ms)",
    y = "Count"
  ) + 
  scale_y_continuous(breaks = scales::pretty_breaks(n = 10)) + 
  scale_x_continuous(breaks = scales::pretty_breaks(n = 6))

### Time and results correlation
full_df %>%
  filter(alg_name == "BrooksAlgorithm") %>%
  filter(num_vertices == 200) %>%
  filter(num_edges == 1000) %>%
  mutate(
    graph_display_name = paste("Graph nr.", graph_internal_id)
  ) %>%
  ggplot(aes(x = time_ms, y = number_of_colors)) +
  geom_point() + 
  facet_grid(cols = vars(graph_display_name), rows = vars(graph_type)) + 
  labs(
    title = "Correlation of time spent to number of colors",
    subtitle = "Found by Brook's Algorithm. Run for 5 random and 5 dense random graphs with 200 nodes and 1000 vertices",
    x = "Time spent (in ms)",
    y = "Number of colors in coloring",
  )

### Compare minimum colorings found
min_colorings <- full_df %>%
  group_by(graph_id, alg_name) %>%
  summarise(
    min_coloring = min(number_of_colors),
    percentage_occurance = sum(
      number_of_colors == min(number_of_colors)
      ) * 100 / length(number_of_colors),
    .groups = "keep"
  ) %>%
  ungroup()

brooks_min_colorings <- min_colorings %>%
  filter(alg_name == "BrooksAlgorithm") %>%
  rename(c(brooks_min = "min_coloring")) %>%
  select(graph_id, brooks_min)
  
cs_min_colorings <- min_colorings %>%
  filter(alg_name == "ConnectedSequential") %>%
  rename(c(cs_min = "min_coloring")) %>%
  select(graph_id, cs_min)


### Finding better solutions
brooks_min_colorings %>%
  left_join(cs_min_colorings, by = "graph_id") %>%
  mutate(
    better = case_when(
      brooks_min < cs_min ~ "BrooksAlgorithm",
      brooks_min > cs_min ~ "ConnectedSequential",
      brooks_min == cs_min ~ "Tie"
    )
  ) %>%
  ggplot(aes(fct_relevel(better, "BrooksAlgorithm", "Tie", "ConnectedSequential"))) +
  geom_bar(fill = "lightblue") + 
  scale_y_continuous(breaks = scales::pretty_breaks(n = 10)) +
  labs(
    title = "Which algorithm found better solution",
    subtitle = "Run for all 150 graphs in a dataset",
    y = "Number of graphs",
    x = "Better algorithm"
  )

min_colorings %>%
  select(alg_name, percentage_occurance) %>%
  group_by(alg_name) %>%
  ggplot(aes(y = percentage_occurance, x = alg_name)) +
  geom_violin(fill = "beige") + 
  scale_y_continuous(breaks = scales::pretty_breaks(n = 10)) + 
  labs(
    title = "Comperation how often each algorithm finds it's best solution",
    subtitle = "Percentage of runs resulted in best coloring for each graph loaded",
    y = "Percentage %",
    x = "Algorithm used"
  )
  


