import unittest
from Team07_CS555_Project import *

class TestUS3BirthBeforeDeath(unittest.TestCase):
    def setUp(self):
        self.family1 = {'F1': {'id': 'F1', 'Husband ID': 'I1', 'Husband Name': 'Allen', 'Husband Lastname': 'Roberts', 'Wife ID': 'I2', 'Wife Name': 'Julie', 'Wife Lastname': 'Jefferson', 'Married': '2012-10-08', 'Divorced': 'NA', 'Children': ['I3']}}
        self.individuals1 = {'I3': {'id': 'I3', 'Name': 'Julie /Jefferson/', 'Gender': 'F', 'Birthday': '2011-10-08', 'Death': '2019-02-11', 'Alive': 'False', 'Child': 'NA', 'Spouse': "{'F1'}", 'Age': 73}}
        self.individuals2 = {'I3': {'id': 'I3', 'Name': 'Julie /Jefferson/', 'Gender': 'F', 'Birthday': '2013-10-08', 'Death': '2019-02-11', 'Alive': 'False', 'Child': 'NA', 'Spouse': "{'F1'}", 'Age': 73}}
        self.family2 = {'F1': {'id': 'F1', 'Husband ID': 'I1', 'Husband Name': 'Allen', 'Husband Lastname': 'Roberts', 'Wife ID': 'I2', 'Wife Name': 'Julie', 'Wife Lastname': 'Jefferson', 'Married': '2012-10-08', 'Divorced': 'NA', 'Children': ['I3']}}
        self.individuals3 = {'I1': {'id': 'I1', 'Name': 'John /Jefferson/', 'Gender': 'M', 'Birthday': '2010-10-08', 'Death': '2019-02-11', 'Alive': 'False', 'Child': 'NA', 'Spouse': "{'F1'}", 'Age': 73}, 'I2': {'id': 'I2', 'Name': 'Julie /Jefferson/', 'Gender': 'F', 'Birthday': '2011-10-08', 'Death': '2019-02-11', 'Alive': 'False', 'Child': 'NA', 'Spouse': "{'F1'}", 'Age': 8}}
        self.individuals4 = {'I1': {'id': 'I1', 'Name': 'John /Jefferson/', 'Gender': 'M', 'Birthday': '1955-10-08', 'Death': '2019-02-11', 'Alive': 'False', 'Child': 'NA', 'Spouse': "{'F1'}", 'Age': 73}, 'I2': {'id': 'I2', 'Name': 'Julie /Jefferson/', 'Gender': 'F', 'Birthday': '1956-10-08', 'Death': '2019-02-11', 'Alive': 'False', 'Child': 'NA', 'Spouse': "{'F1'}", 'Age': 73}}
        self.family3 = {'F1': {'id': 'F1', 'Husband ID': 'I1', 'Husband Name': 'Allen', 'Husband Lastname': 'Roberts', 'Wife ID': 'I2', 'Wife Name': 'Julie', 'Wife Lastname': 'Jefferson', 'Married': '2012-10-08', 'Divorced': 'NA', 'Children': ['I3']},'F2': {'id': 'F2', 'Husband ID': 'I1', 'Husband Name': 'Allen', 'Husband Lastname': 'Roberts', 'Wife ID': 'I4', 'Wife Name': 'Honey', 'Wife Lastname': 'Jefferson', 'Married': '2012-10-08', 'Divorced': 'NA', 'Children': ['I3']}}
        self.individuals5 = {'I1': {'id': 'I1', 'Name': 'John /Jefferson/', 'Gender': 'M', 'Birthday': '2010-10-08', 'Death': '2019-02-11', 'Alive': 'False', 'Child': 'NA', 'Spouse': "{'F1'}", 'Age': 73}, 'I2': {'id': 'I2', 'Name': 'Julie /Jefferson/', 'Gender': 'F', 'Birthday': '2011-10-08', 'Death': '2019-02-11', 'Alive': 'False', 'Child': 'NA', 'Spouse': "{'F1'}", 'Age': 8}, 'I3': {'id': 'I3', 'Name': 'Honey /Jefferson/', 'Gender': 'F', 'Birthday': '2011-10-08', 'Death': '2019-02-11', 'Alive': 'False', 'Child': 'NA', 'Spouse': "{'F2'}", 'Age': 8}}
        self.individuals6 = {'I1': {'id': 'I1', 'Name': 'John /Jefferson/', 'Gender': 'M', 'Birthday': '1955-10-08', 'Death': '2019-02-11', 'Alive': 'False', 'Child': 'NA', 'Spouse': "{'F1'}", 'Age': 73}, 'I2': {'id': 'I2', 'Name': 'Julie /Jefferson/', 'Gender': 'F', 'Birthday': '1956-10-08', 'Death': '2019-02-11', 'Alive': 'False', 'Child': 'NA', 'Spouse': "{'F1'}", 'Age': 73}}
        self.family4 = {'F1': {'id': 'F1', 'Husband ID': 'I1', 'Husband Name': 'Allen', 'Husband Lastname': 'Roberts', 'Wife ID': 'I2', 'Wife Name': 'Julie', 'Wife Lastname': 'Jefferson', 'Married': '2012-10-08', 'Divorced': 'NA', 'Children': ['I3']}}
        self.individuals7 = {'I1': {'id': 'I1', 'Name': 'John /Jefferson/', 'Gender': 'M', 'Birthday': '1955-10-08', 'Death': '2019-02-11', 'Alive': 'False', 'Child': 'NA', 'Spouse': "{'F1'}", 'Age': 73}, 'I2': {'id': 'I2', 'Name': 'Julie /Jefferson/', 'Gender': 'F', 'Birthday': '1956-10-08', 'Death': '2019-02-11', 'Alive': 'False', 'Child': 'NA', 'Spouse': "{'F1'}", 'Age': 73}, 'I3': {'id': 'I3', 'Name': 'Johnny /Jefferson/', 'Gender': 'M', 'Birthday': '2020-10-08', 'Death': '2021-02-11', 'Alive': 'False', 'Child': 'NA', 'Spouse': "{'F3'}", 'Age': 1}}
        self.individuals8 = {'I1': {'id': 'I1', 'Name': 'John /Jefferson/', 'Gender': 'M', 'Birthday': '1955-10-08', 'Death': '2019-02-11', 'Alive': 'False', 'Child': 'NA', 'Spouse': "{'F1'}", 'Age': 73}, 'I2': {'id': 'I2', 'Name': 'Julie /Jefferson/', 'Gender': 'F', 'Birthday': '1956-10-08', 'Death': '2019-02-11', 'Alive': 'False', 'Child': 'NA', 'Spouse': "{'F1'}", 'Age': 73}, 'I3': {'id': 'I3', 'Name': 'Johnny /Jefferson/', 'Gender': 'M', 'Birthday': '1990-10-08', 'Death': '2021-02-11', 'Alive': 'False', 'Child': 'NA', 'Spouse': "{'F3'}", 'Age': 31}}
        self.family5 = {'F1': {'id': 'F1', 'Husband ID': 'I1', 'Husband Name': 'Allen', 'Husband Lastname': 'Roberts', 'Wife ID': 'I2', 'Wife Name': 'Julie', 'Wife Lastname': 'Jefferson', 'Married': '2012-10-08', 'Divorced': 'NA', 'Children': ['I3', 'I4']}}
        self.individuals9 = {'I1': {'id': 'I1', 'Name': 'John /Jefferson/', 'Gender': 'M', 'Birthday': '1955-10-08', 'Death': '2019-02-11', 'Alive': 'False', 'Child': 'NA', 'Spouse': "{'F1'}", 'Age': 73}, 'I2': {'id': 'I2', 'Name': 'Julie /Jefferson/', 'Gender': 'F', 'Birthday': '1956-10-08', 'Death': '2019-02-11', 'Alive': 'False', 'Child': 'NA', 'Spouse': "{'F1'}", 'Age': 73}, 'I3': {'id': 'I3', 'Name': 'Johnny /Jefferson/', 'Gender': 'M', 'Birthday': '2020-10-08', 'Death': '2021-02-11', 'Alive': 'False', 'Child': 'NA', 'Spouse': "{'F3'}", 'Age': 1}, 'I4': {'id': 'I4', 'Name': 'Johnny /Jefferson/', 'Gender': 'M', 'Birthday': '2020-11-08', 'Death': '2021-02-11', 'Alive': 'False', 'Child': 'NA', 'Spouse': "{'F3'}", 'Age': 1}}
        self.family6 = {'F1': {'id': 'F1', 'Husband ID': 'I1', 'Husband Name': 'Allen', 'Husband Lastname': 'Roberts', 'Wife ID': 'I2', 'Wife Name': 'Julie', 'Wife Lastname': 'Jefferson', 'Married': '2012-10-08', 'Divorced': 'NA', 'Children': ['I3', 'I4', 'I5', 'I6', 'I7', 'I8']}}
        self.individuals10 = {'I1': {'id': 'I1', 'Name': 'John /Jefferson/', 'Gender': 'M', 'Birthday': '1955-10-08', 'Death': '2019-02-11', 'Alive': 'False', 'Child': 'NA', 'Spouse': "{'F1'}", 'Age': 73}, 'I2': {'id': 'I2', 'Name': 'Julie /Jefferson/', 'Gender': 'F', 'Birthday': '1956-10-08', 'Death': '2019-02-11', 'Alive': 'False', 'Child': 'NA', 'Spouse': "{'F1'}", 'Age': 73}, 'I3': {'id': 'I3', 'Name': 'Johnny /Jefferson/', 'Gender': 'M', 'Birthday': '2020-10-08', 'Death': '2021-02-11', 'Alive': 'False', 'Child': 'NA', 'Spouse': "{'F3'}", 'Age': 1}, 'I4': {'id': 'I4', 'Name': 'Johnny /Jefferson/', 'Gender': 'M', 'Birthday': '2020-11-08', 'Death': '2021-02-11', 'Alive': 'False', 'Child': 'NA', 'Spouse': "{'F3'}", 'Age': 1}, 'I5': {'id': 'I5', 'Name': 'Johnny /Jefferson/', 'Gender': 'M', 'Birthday': '2020-10-08', 'Death': '2021-02-11', 'Alive': 'False', 'Child': 'NA', 'Spouse': "{'F3'}", 'Age': 1}, 'I6': {'id': 'I6', 'Name': 'Johnny /Jefferson/', 'Gender': 'M', 'Birthday': '2020-11-08', 'Death': '2021-02-11', 'Alive': 'False', 'Child': 'NA', 'Spouse': "{'F3'}", 'Age': 1}, 'I7': {'id': 'I7', 'Name': 'Johnny /Jefferson/', 'Gender': 'M', 'Birthday': '2020-10-08', 'Death': '2021-02-11', 'Alive': 'False', 'Child': 'NA', 'Spouse': "{'F3'}", 'Age': 1}, 'I8': {'id': 'I8', 'Name': 'Johnny /Jefferson/', 'Gender': 'M', 'Birthday': '2020-11-08', 'Death': '2021-02-11', 'Alive': 'False', 'Child': 'NA', 'Spouse': "{'F3'}", 'Age': 1}}
        self.family7 = {'F1': {'id': 'F1', 'Husband ID': 'I1', 'Husband Name': 'Allen', 'Husband Lastname': 'Roberts', 'Wife ID': 'I2', 'Wife Name': 'Julie', 'Wife Lastname': 'Jefferson', 'Married': '2012-10-08', 'Divorced': 'NA', 'Children': ['I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9', 'I10', 'I11', 'I12', 'I13', 'I14','I15', 'I16', 'I17', 'I18', 'I19', 'I20']}}
        self.family8 = {'F1': {'id': 'F1', 'Husband ID': 'I1', 'Husband Name': 'Allen', 'Husband Lastname': 'Bairstow', 'Wife ID': 'I2', 'Wife Name': 'Julie', 'Wife Lastname': 'Jefferson', 'Married': '2012-10-08', 'Divorced': 'NA', 'Children': ['I19']}}
        self.individuals11 = {'I1': {'id': 'I1', 'Name': 'Jhonny', 'Lastname': 'Bairstow', 'Gender': 'M', 'Birthday': '1900-03-02', 'Death': 'NA', 'Alive': 'True', 'Child': "{'F1'}", 'Spouse': 'NA', 'Age': 123}, 'I19': {'id': 'I19', 'Name': 'Jhonny', 'Lastname': 'Roberts', 'Gender': 'M', 'Birthday': '1900-03-02', 'Death': 'NA', 'Alive': 'True', 'Child': "{'F5'}", 'Spouse': 'NA', 'Age': 123}}
        self.family9 = {'F1': {'id': 'F1', 'Husband ID': 'I1', 'Husband Name': 'Allen', 'Husband Lastname': 'Roberts', 'Wife ID': 'I2', 'Wife Name': 'Julie', 'Wife Lastname': 'Jefferson', 'Married': '2012-10-08', 'Divorced': 'NA', 'Children': ['I3']},'F2': {'id': 'F1', 'Husband ID': 'I1', 'Husband Name': 'Allen', 'Husband Lastname': 'Roberts', 'Wife ID': 'I4', 'Wife Name': 'Honey', 'Wife Lastname': 'Jefferson', 'Married': '2012-10-08', 'Divorced': 'NA', 'Children': ['I3']}}
        self.individuals12 = {'I3': {'id': 'I3', 'Name': 'Julie /Jefferson/', 'Gender': 'M', 'Birthday': '2011-10-08', 'Death': '2019-02-11', 'Alive': 'False', 'Child': 'NA', 'Spouse': "{'F1'}", 'Age': 73}}
    def test_US9_1(self):
        Error01= US09_birth_before_death_of_parents(self.family1, self.individuals1)
        self.assertEqual(Error01, ['ERROR US09: I3 Julie /Jefferson/ 2011-10-08'])
        
    def test_US9_2(self):
        Error02= US09_birth_before_death_of_parents(self.family1, self.individuals2)
        self.assertEqual(Error02, [])

    def test_US10_1(self):
        Error03 = US10_marriage_after_14(self.family2, self.individuals3)
        self.assertEqual(Error03, ['I2', 'I1'])
    
    def test_US10_2(self):
        Error04 = US10_marriage_after_14(self.family2, self.individuals4)
        self.assertEqual(Error04, [])

    def test_US11_1(self):
        Error05= US11_No_Bigamy(self.family3, self.individuals5)
        self.assertEqual(Error05, ['ERROR US11: Bigamy detected for husband I1 in family F2'])
    
    def test_US11_2(self):
        Error06= US11_No_Bigamy(self.family2, self.individuals6)
        self.assertEqual(Error06, [])

    def test_US12_1(self):
        Error07 = US12_Parents_not_too_old(self.family4, self.individuals7)
        self.assertEqual(Error07, ['Child I3 has parents too old to him'])
    
    def test_US12_2(self):
        Error08 = US12_Parents_not_too_old(self.family4, self.individuals8)
        self.assertEqual(Error08, [])
    
    def test_US13_1(self):
        Error09= US13_siblings_spacing(self.individuals9, self.family5)
        self.assertEqual(Error09, ["Sibling birthdays should be less than 2 days apart or greater than 8 months apart.\nChild IDs with Error: ['I3', 'I4']"])
        
    def test_US14_1(self):
        Error10 = US14_multiple_births_less_than_5(self.individuals10, self.family6)
        self.assertEqual(Error10, ["No more than five siblings should be born at the same time.\n Child IDs with Error: ['I3', 'I4', 'I5', 'I6', 'I7', 'I8']"])
    
    def test_US15_1(self):
        Error11= US15_Fewer_than_15_siblings(self.family7)
        self.assertEqual(Error11, ["ERROR US15: F1 has 18 siblings, which is more than 15."])

    def test_US16_1(self):
        Error12 = US16_Male_Last_Name(self.individuals11, self.family8)
        self.assertEqual(Error12, ["ERROR US16: Jhonny has a different last name: Roberts than the father's last name: Bairstow"])
    
    def test_US21_1(self):
        Error21 = US21_correct_gender_for_role(self.individuals1, self.family1)
        self.assertEqual(Error21, [])
    
    def test_US21_2(self):
        Error21 = US21_correct_gender_for_role(self.individuals12, self.family9)
        self.assertEqual(Error21, [])

    def test_US22_1(self):
        Error22 = US22_unique_IDs(self.individuals12, self.family9)
        self.assertEqual(Error22, [])

    def test_US22_2(self):
        Error22 = US22_unique_IDs(self.individuals1, self.family1)
        self.assertEqual(Error22, [])
    
if __name__ == '__main__':
    unittest.main()
