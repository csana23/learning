# adat import
# klasszikus Boston Housing Dataset
# cel: lakas median ertekenek megadasa ezer dollarban (medv oszlop)
# tobbvaltozos linearis modell alapjan
require(MASS)
library(MASS)
data = Boston
data

# EDA - exploratoty data analysis
# csekkoljuk van-e NULL ertek
any(is.na(data))

summary(data)
dim(data)
head(data)

# mit jelentenek az oszlopok
# crim: bűnözési ráta per fő
# zn: 25000 sqft feletti lakótelepek aránya
# indus: ipari terület aranya kisvarosonkent holdban (kivalo angolszasz mertekegysegek...)
# chas: 1 ha folyot erint a telek, 0 ha nem
# nox: nitrogen-oxidok koncentracioja
# rm: szobak atlagos szama per lakas
# age: 1940 elott epitett lakasok aranya
# dis: 5 bostoni business centerhez viszonyitott tavolsagok sulyozott atlaga
# rad: autopalyak elerhetosegi indexe
# tax: ingatlan ado rata 10 ezer dollaronkent
# ptratio: iskolas-tanar rata kisvarosonkent
# black: feketek aranya kisvarosonkent
# lstat: populacio alacsony statuszu tagjainak aranya
# medv: lakasok median erteke ezer dollarban 

# lathatjuk, hogy az adatok egy resze aranyszam, igy nem feltetlenul
# kompatibilis a feature (megjosolando) attributummal
# azonban nem lattam olyan publikaciot, amiben ezt megemlitettek volna, mint problema, illetve
# ahhoz, hogy ezt kezelni tudjuk, a linearis modelltol eltero modellre lenne szuksegunk
# igy eredeti formajukban hasznalom oket
# https://www.theanalysisfactor.com/proportions-as-dependent-variable-in-regression-which-type-of-model/

# outlier kereses boxplot-al
# meghivom az egesz dataframe-re, hogy eldonthessuk melyeket erdemes kihagyni
# cel a jo altalanositas
boxplot(data)

# ennek megfeleloen elhagyjuk a kovetkezo attributumokat
# illetve termeszetesen az etnikai kisebbsegeket nem erheti hatranyos megkulonboztetes
data = subset(data, select=-c(crim, zn, black))
head(data)

# vizualizacio
data_num = data.matrix(data)
data_num

pairs(data_num)

# ranezesre linearis kapcsolata a medv attr-al ezeknek az oszlopoknak van:
# rm, lstat, ptratio - azonban meghagyjuk mindegyik oszlopot es
# majd az attributum kivalasztasnal eldol, igazunk volt-e (tehat, hogy csak ezek maradnak
# benne a modellben) 
# train-test split - beallitunk seed-et, hogy reprodukalhato legyen
set.seed(101)
sample = sample.int(n=nrow(data), size=floor(.75*nrow(data)), replace = F)

data_train = data[sample, ]
data_test = data[-sample, ]

summary(data_train)
summary(data_test)

dim(data_train)
dim(data_test)

# mivel tobb attributumot veszunk bele a modellbe, igy nehany ellenorzo lepest kell tennunk
# az egyes attributumok fuggetlenek legyenek egymastol
# multikollinearitás elkerulese
# eloszor is letrehozzuk a kezdeti modellt, amelyben minden attributum benne van
linear_model = lm(medv~., data=data_train)
linear_model

# aztan stepwise regression-t (with AIC statistics) hasznalunk - MASS libraryben bent van
# ez kezeli a multikollinearitást is
# direction both, azaz a forward és backward kevereket hasznaljuk
step_linear_model = stepAIC(linear_model, direction="both", trace=TRUE)

# igy megkapjuk a vegso modellunket
step_linear_model

# ertekeljuk a kapott modellt
summary(step_linear_model)

# t-value vs p-value
# az osszes t-value 0-tol elter, igy tenylegesen hatassal vannak az egyes attributumok
# a median haz arra
# a p-value mindegyiknel szignifikansan alacsony, igy a t-value ertekei nem veletlenul alakultak igy
# azaz az alternativ hipotezis a nyero: H1 - ami azt mondja, hogy az egyes fuggetlen attributumok
# es a fuggo attributum kozott van osszefugges
# a kovetkezo statisztika, amit megnezunk az adjusted r-squared
# azert, mert ez kezeli az R2 erteket tobb attributum eseten
# a modellunk a variancia 71%-at kepes megmagyarazni
# elfogadjuk a modellt, most pedig teszteljuk a teszt adatokon

# predict ertekek modell alapjan, aztan megnezzuk hogyan viszonyulnak az eredeti teszt ertekekhez
predicted = predict(step_linear_model, data_test)
length(predicted)

# megvannak a predicted ertekek
# megnezzuk a josagi mertekeket a train es test adathalmazra
require(ModelMetrics)
library(ModelMetrics)

actual_train = as.numeric(data_train$medv)
predicted_train = step_linear_model$fitted.values

actual_test = as.numeric(data_test$medv)
predicted_test = predicted

plot(actual_train)
lines(predicted_train, col="red", lty="dotted")
text(20,10, "predicted values", col="red")

plot(actual_test)
lines(predicted_test, col="red", lty="dotted")
text(20,10, "predicted values", col="red")

rmse_train = ModelMetrics::rmse(actual_train, predicted_train, step_linear_model)
rmse_test = ModelMetrics::rmse(actual_test, predicted_test, step_linear_model)
print("RMSE train: ")
print(rmse_train)
print("RMSE test: ")
print(rmse_test)

mse_train = ModelMetrics::mse(actual_train, predicted_train, step_linear_model)
mse_test = ModelMetrics::mse(actual_test, predicted_test, step_linear_model)
print("MSE train: ")
print(mse_train)
print("MSE test: ")
print(mse_test)

mae_train = ModelMetrics::mae(actual_train, predicted_train, step_linear_model)
mae_test = ModelMetrics::mae(actual_test, predicted_test, step_linear_model)
print("MAE train: ")
print(mae_train)
print("MAE test: ")
print(mae_test)

# ertekeles
# az egyes hiba mertekek kozel vannak egymashoz, igy lathatjuk,
# hogy a modell jól általánosít, nem beszélhetünk under-, vagy overfittingről

# megnezunk egy masik megkozelitest, evvel konnyeben tudjuk tesztelni az uj modell
# teljesitmenyet
# k-fold cross validation a modell teljesitmenyenek atfogo tesztelesere
# 10-szer valasztunk random meretu train es teszt halmazt (az eredeti adathalmaz 75%-aban) es ennek az eredmenyet teszteljuk a teszt adathalmazon
# ugyanugy felosztjuk az adathalmazt train-test reszekre
require(caret)
library(caret)

data = Boston
data

# most benne hagyunk minden attributumot, megnezzuk jobb r2-et kapunk-e
set.seed(101)
sample = sample.int(n=nrow(data), size=floor(.75*nrow(data)), replace = F)

data_train = data[sample, ]
data_test = data[-sample, ]

dim(data_train)

train_control = trainControl(method="cv", number=10) # 10 kort futunk az algoritmussal

cv_linear_model = train(medv~., data=data_train, method="lm", trControl=train_control)

cv_linear_model

# predict on test set
predicted_cv = predict(cv_linear_model, data_test)
predicted_cv

actual_test = as.numeric(data_test$medv)
predicted_test = predicted_cv 

# rmse test adatokon  
rmse_cv_test = ModelMetrics::rmse(actual_test, predicted_test, cv_linear_model)
rmse_cv_test

# a train dataset-re az rmse 4,62; a teszt dataset-re 5,4

mae_cv_test = mae_test = ModelMetrics::mae(actual_test, predicted_test, cv_linear_model)
mae_cv_test

# a train dataset-re a mae 3,3; a teszt dataset-re 3,73

# a modellek teljesitmenye a ket megkozelitessel is hasonlo,
# ebbol latszik, hogy az elso modellbol (step_linear_model) elhagyott
# attributumok nem befolyasoltak jelentosen a modell teljesitmenyet - tehat tenyleg elhanyagolhatoak

# osszefoglalas
# mivel az attributumok nagy resze arany szam, így a tovabb fejlesztesben preferalt lenne
# esetleg egy logistic regression modellt hasznalni







































