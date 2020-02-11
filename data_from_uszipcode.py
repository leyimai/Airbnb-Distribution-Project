from uszipcode import SearchEngine
import pandas as pd 
import numpy as np
def get_population_df(zipcodes):
    search = SearchEngine(simple_zipcode=False)
    #feature_df= pd.DataFrame()
    age_df= pd.DataFrame()
    race_df = pd.DataFrame()
    householdincome_df=pd.DataFrame()
   
    for z in zipcodes:
        result = search.by_zipcode(z)
        if result.population_by_age:
            a = pd.DataFrame(result.population_by_age[2]['values']).set_index('x').T 
            a['zipcode']=z
            age_df = pd.concat([age_df,a])
        if result.population_by_race:
            r = pd.DataFrame(result.population_by_race[0]['values']).set_index('x').T                                 
            r['zipcode'] = z
            race_df= pd.concat([race_df,r])
        if result.household_income:
            h = pd.DataFrame(result.household_income[0]['values']).set_index('x').T
            h['zipcode']=z 
            householdincome_df=pd.concat([householdincome_df,h])
            
    return age_df,race_df,householdincome_df

def population_final(age_df,race_df,householdincome_df):
    
    age_df = age_df.set_index('zipcode')
    age_df.columns = [f'age:{col}' for col in age_df.columns]
        
    #age_df['num_of_children'] = age_df['Under 5'] +age_df['5-9']+age_df['10-14']+age_df['15-19']
    age_df['total_population'] = age_df.apply(sum,axis=1)
    #age_df= age_df[['zipcode','total_population','num_of_children','20-24','25-29','30-34','35-39']]
    
    race_df= race_df[['zipcode','White','Black Or African American','American Indian Or Alaskan Native', 'Asian']]
    
    householdincome_df = householdincome_df.set_index('zipcode')
    householdincome_df['total'] =householdincome_df.apply(sum,axis=1)
    for col in householdincome_df.columns:
        householdincome_df[f'householdincome{col}_percent']=householdincome_df[col]/householdincome_df['total']
    #householdincome_df.drop(columns=incomes)
    
    final_df = pd.merge(age_df,race_df,left_index=True,right_on='zipcode',copy=False)
    final_df = pd.merge(final_df,householdincome_df,left_on='zipcode',right_index=True,copy=False)
    final_df = final_df.set_index('zipcode')
    return final_df


def get_edu_employ_df(zipcodes):

    search = SearchEngine(simple_zipcode=False)
    #feature_df= pd.DataFrame()
    education_df= pd.DataFrame()
    employ_df = pd.DataFrame()
    for z in zipcodes:
        result = search.by_zipcode(z)
        if result.population_by_age:
            a = pd.DataFrame(result.educational_attainment_for_population_25_and_over[0]['values']).set_index('x').T 
            a['zipcode']=z
            education_df = pd.concat([education_df,a])
        if result.employment_status:
            b = pd.DataFrame(result.employment_status[0]['values']).set_index('x').T
            b['zipcode']=z
            employ_df = pd.concat([employ_df,b])
    return education_df,employ_df
    
def edu_employ_final(education_df,employ_df):
    for df in [education_df,employ_df]:
        df.set_index('zipcode',inplace=True)
        columns = [x.lower().replace(' ','_') for x in df.columns]
        df.columns=columns
        df['total']=df.apply(sum,axis=1)
        for col in columns:
            df[f'{col}_percent']=df[col]/df['total']
        df.drop(columns='total',inplace=True)
    final_df = pd.merge(education_df,employ_df,copy=False,left_index=True,right_index=True)
    return final_df


def get_estate_df(zipcodes):
    search = SearchEngine(simple_zipcode=False)
    dict_ = {}    
    for zipcode in zipcodes:
        column_list = ['housing_units', 'occupied_housing_units', 'median_home_value']
        # zipcode = str(int(zipcode))
        
        dict_[zipcode] = list()
        data = search.by_zipcode(zipcode)
        data_dict = data.to_dict()
        dict_[zipcode].append(data_dict['housing_units'])
        dict_[zipcode].append(data_dict['occupied_housing_units'])
        dict_[zipcode].append(data_dict['median_home_value'])
        
        #year_housing_was_built
        try:
            for i in data_dict['year_housing_was_built'][0]['values']:
                dict_[zipcode].append(i['y'])
                column_list.append('year_housing_was_built: ' + i['x'])
        except:
            for i in range(9):
                dict_[zipcode].append('np.NaN')
        
        #'housing_occupancy'    
        try:
            for i in data_dict['housing_occupancy'][0]['values']:
                dict_[zipcode].append(i['y'])
                column_list.append('housing_occupancy: ' + i['x'])
        except:
            for i in range(4):
                dict_[zipcode].append('np.NaN')
        
        #vancancy_reason
        try:
            for i in data_dict['vancancy_reason'][0]['values']:
                dict_[zipcode].append(i['y'])
                column_list.append('vancancy_reason: ' + i['x'])
        except:
            for i in range(7):
                dict_[zipcode].append('np.NaN')
        
        #owner_occupied_home_values
        try:
            for i in data_dict['owner_occupied_home_values'][0]['values']:
                dict_[zipcode].append(i['y'])
                column_list.append('owner_occupied_home_values: ' + i['x'])
        except:
            for i in range(8):
                dict_[zipcode].append('np.NaN')
        
        #rental_properties_by_number_of_rooms
        try:
            for i in data_dict['rental_properties_by_number_of_rooms'][0]['values']:
                dict_[zipcode].append(i['y'])
                column_list.append('rental_properties_by_number_of_rooms: ' + i['x'])
        except:
            for i in range(4):
                dict_[zipcode].append('np.NaN')
                
        #monthly_rent_including_utilities_studio_apt
        try:
            for i in data_dict['monthly_rent_including_utilities_studio_apt'][0]['values']:
                dict_[zipcode].append(i['y'])
                column_list.append('monthly_rent_including_utilities_studio_apt: ' + i['x'])
        except:
            for i in range(6):
                dict_[zipcode].append('np.NaN')
        
        #monthly_rent_including_utilities_1_b
        try:
            for i in data_dict['monthly_rent_including_utilities_1_b'][0]['values']:
                dict_[zipcode].append(i['y'])
                column_list.append('monthly_rent_including_utilities_1_b: ' + i['x'])
        except:
            for i in range(6):
                dict_[zipcode].append('np.NaN') 
        
        #monthly_rent_including_utilities_2_b
        try:
            for i in data_dict['monthly_rent_including_utilities_2_b'][0]['values']:
                dict_[zipcode].append(i['y'])
                column_list.append('monthly_rent_including_utilities_2_b: ' + i['x'])
        except:
            for i in range(6):
                dict_[zipcode].append('np.NaN')        
        
        #monthly_rent_including_utilities_3plus_b
        try:
            for i in data_dict['monthly_rent_including_utilities_3plus_b'][0]['values']:
                dict_[zipcode].append(i['y'])
                column_list.append('monthly_rent_including_utilities_3plus_b: ' + i['x'])
        except:
            for i in range(6):
                dict_[zipcode].append('np.NaN')
                
    real_estate = pd.DataFrame.from_dict(dict_, orient = 'index', 
                                         columns = column_list)
    #real_estate.replace('NaN',np.NaN)
    
    #real_estate['zipcode'] = real_estate.index
    
    return real_estate