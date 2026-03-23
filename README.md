**Group Project on data parsing, EDA and building ML model for Auto market. Based on parsing of Auto.ru website**

**Steps of project:**
1. Gather data using web scrapping (Selenium+BS4)
2. Enrich data using other API (geography, climate, social-economic indicators)
3. EDA
4. Building an ML model to prognose price for a car

**Price** is a target variable

**Main features:**
1.Technical specifications(year of manufacture, mileage, engine capacity, power)
2. Geographical data (city, latitude,longitude)
3. Social-economic indicators (population, salary, infrastructure)
4. Climatic conditions (temperature, air quality)

**How to use?**
Activate venv and download libraries
python3 -m venv venv
pip3 install -r requirements.txt
_Now code is ready to run_

**Main stages in details:**
Parsing: in file auto_ru_parsing.py. What is going on?
1. Selenium driver works with Chrome
2. For each city (Moscow, St. Petersburg, Novosibirsk), 100 pages with ads are loaded, then the infinite scroll is going untill we are too far from exact city
3. BeautifulSoup parses HTML car cards.
4. The main characteristics are extracted: name, price, year, mileage, specs
5. Saved in dataset on each city and merged in 'res_dataset_cars.csv'
What is special?
1. Random delays between requests (1 to 5 seconds) to avoid blocking
2. Infinite scrolling on the last page for completeness of data
3. Link uniqueness checkong
4. Logging of all operations in `auto_ru_parser.log` with logging module

**API:** in file API_extra_v3.ipynb. What is going on?
1. API providers are found, links established.
2. Data is found
3. Creating and merging the enriched table with additional features 'final_api_and_scraping_merged.csv'
4. Data with API
   -Latitude, Longitude by city name
   -Temperature
   -Air quality
   -Population
   -Salary
   -Mestnost (Terrain)
   -Infrastructure (presence of maintenance points)
**EDA:** in file 'EDA.ipynb'
1. Clean the data
2. Create new features from specs and name
   -Extracting the brand and model from the car name
   -Parsing of the 'specs' column to obtain technical characteristics:
   -'class' — car class (sedan, SUV, hatchback, etc.)
   -'drive' — drive (FWD, RWD, AWD)
   -'gearbox' — gearbox (automatic, manual, etc.)
   -'fuel_type' — type fuel (gasoline, diesel, electric)
   -'engine_volume' — engine displacement
   -'engine_power' — engine h.p.
3. Outliers handling
4. Analyze dataset statistics
5. Create vizualisations
Result: 'eda.csv'

**ML:**
'ML_final.ipynb'
1. Chosing the model: CatBoost is a basic model with categorical variable processing
2. Feature engineering
2. Division into training and test samples
3. Model training with hyperparameter optimization
4. Quality assessment(MAE)
5. Analysis of the importance of features

**DATA DESCRIPTION:**
### Source data file: res_dataset_cars.csv with size (12628,8)
Target: price(continuous numeric variable)
Discrete numeric variables: year (ordinal)
Nominal categorical variables:name (categorical, high diversity),city (categorical), seller(categorical, high diversity), link (categorical, unique)
Text variables that require preprocessing: mileage, specs
**At this stage, the data contains a significant amount of noise and needs to be cleaned.**

What we got after API and EDA:
**eda.csv with size (10,772,21)**

Target variable for forecasting:
- price (continuous) — target variable for regression analysis

Numerical:
Continuous variables:
mileage (after parsing from the text form) — mileage in kilometers, range 0-850,000 km, asymmetric distribution
engine_volume, engine volume in liters
engine_power, engine power in horsepower
temperature, the average annual temperature of the city
air_quality, air quality index
salary , the average salary in the city
population, population size

Discrete numeric variables:
year (discrete ordinal),the cars year of manufacture

Coordinate variables:
latitude and longitude, geographical location

Nominal categorical variables
city,location city
class, class of car, about 6 categories (sedan, SUV, hatchback, wagon, coupe, others)
drive, drivetrain type, 3 categories (FWD, RWD, AWD)
gearbox,gearbox type, 2 categories (automatic, manual)
fuel_type, fuel type, 3 main categories (petrol, diesel, hybrid)
seller, seller name
brand, manufacturer's brand, with more than 50 unique values
model, a car model with several hundred unique values

Ordinal variables:
mestnost, typology of the area from rural to urban (0-5)
infrastructure, infrastructure development in city (0-500)


  
