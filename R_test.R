install.packages("FactoMineR")
install.packages("vcd")
install.packages("factoextra")
install.packages("ClusterR")
install.packages("cluster")
install.packages("dplyr")
install.packages("ggbeeswarm")
install.packages("explore")
install.packages("missMDA")
install.packages("ggfortify")

library(readxl)
library(FactoMineR)
library(vcd)
library(ggplot2)
library(ggbeeswarm)
library(factoextra)
library(cluster)
library(ClusterR)
library(dplyr)
library(explore)
library(missMDA)
library(ggfortify)
# Importing data from Excel sheets
pdt_data = read_excel('D:/Y4S2/MA4829 Machine Intel/proj/MA4829-machine-intelligence-project/stringed_survey.xlsx')
range_data = read_excel('D:/Y4S2/MA4829 Machine Intel/proj/MA4829-machine-intelligence-project/range_survey.xlsx')
encoded_data = read_excel('D:/Y4S2/MA4829 Machine Intel/proj/MA4829-machine-intelligence-project/encoded_data.xlsx')

multiplesheets <- function(fname) {
    # getting info about all excel sheets
  sheets <- readxl::excel_sheets(fname)
  tibble <- lapply(sheets, function(x) readxl::read_excel(fname, sheet = x))
  data_frame <- lapply(tibble, as.data.frame)
    # assigning names to data frames
  names(data_frame) <- sheets
    # print data frame
  print(data_frame)
}
# specifying the path name
path <- "D:/Y4S2/MA4829 Machine Intel/proj/MA4829-machine-intelligence-project/factors.xlsx"
factors = multiplesheets(path)


# removing column number from dataset
pdt_data = pdt_data[c(2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18)]

# preliminary scatterplots to see any obvious trends and structure of dataframes
plot(pdt_data)
plot(range_data)
plot(encoded_data)

str(pdt_data)
str(range_data)
str(encoded_data)
str(factors)

encoded_data %>% 
  explore_all()

encoded_data %>% 
  select(Age_label_encoded, fact_length, ext_length, int_length, PersonalizationJob_label_encoded, WTSCustomization_label_encoded, WTSPersonalization_label_encoded, WantOwnPersonalization_label_encoded) %>% 
  explore_all(target = Age_label_encoded)

encoded_data %>% 
  select(Category_label_encoded, fact_length, ext_length, int_length, PersonalizationJob_label_encoded, WTSCustomization_label_encoded, WTSPersonalization_label_encoded, WantOwnPersonalization_label_encoded) %>% 
  explore_all(target = Category_label_encoded)

encoded_data %>% 
  select(Gender_label_encoded, fact_length, ext_length, int_length, PersonalizationJob_label_encoded, WTSCustomization_label_encoded, WTSPersonalization_label_encoded, WantOwnPersonalization_label_encoded) %>% 
  explore_all(target = Gender_label_encoded)

encoded_data %>% 
  select(MarriageStatus_label_encoded, fact_length, ext_length, int_length, PersonalizationJob_label_encoded, WTSCustomization_label_encoded, WTSPersonalization_label_encoded, WantOwnPersonalization_label_encoded) %>% 
  explore_all(target = MarriageStatus_label_encoded)


# Trying out Principal Component Analysis for encoded_data since all numeric (failed)
# my_pca <- prcomp(encoded_data, scale = TRUE,
#                 center = TRUE, retx = T)


# Trying out factor analysis of encoded data (Looking for Principal Component)
encode <- imputePCA(encoded_data, ncp = 2, scale = TRUE, method = c("Regularized"), 
          row.w = NULL, ind.sup=NULL,quanti.sup=NULL,quali.sup=NULL,
          coeff.ridge = 1, threshold = 1e-06, seed = NULL, nb.init = 1,  
          maxiter = 1000)
# encoded_famd <- FAMD(encoded_data, graph=TRUE)
encode <- imputePCA(encoded_data)
encode.pca <- PCA(encode['completeObs'])


########
# Replacing NA values with 0 and running PCA on encoded data
encoded_data[is.na(encoded_data)] <- 0
first.pca <- prcomp(encoded_data[,c(1:12)],
                   center = TRUE,
                   scale. = TRUE)


#Plotting scree plot of PCA
var_explained = first.pca$sdev^2 / sum(first.pca$sdev^2)
qplot(c(1:12), var_explained) + geom_line() + xlab("Principal Component") + ylab("Variance Explained") + ggtitle("Scree Plot") + ylim(0, 1)
# Summary of PCA
summary(first.pca)

# Plotting PCA plot (probably looks better)
first.pca.plot <- autoplot(first.pca,
                           data = encoded_data, loadings = TRUE, loadings.colour = 'blue', loadings.label = TRUE)
first.pca.plot

# Plotting PCA plot with labelled data points in background
first.pca.biplot <- biplot(first.pca,
                            data = encoded_data, loadings = TRUE, loadings.colour = 'blue', loadings.label = TRUE)
first.pca.biplot

# Plot of all 10 primary components and variance in data
plot.pca.variance <- plot(first.pca, type="l")
plot.pca.variance

# Trying out factor analysis of mixed data since dataframe consists of both numerical and categorical data (failed)
# pdt_famd <- FAMD(pdt_data, graph=TRUE)
# range_famd <- FAMD(range_data, graph=TRUE)
