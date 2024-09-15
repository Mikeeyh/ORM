from sqlalchemy.orm import sessionmaker
import random
from models import Employee, engine, City
from sqlalchemy import or_, and_, not_

Session = sessionmaker(bind=engine)
with Session() as session:
    """Adding single record"""
#     employee = Employee(
#         first_name="Mike",
#         last_name="Haralanov",
#         age=25
#     )
#     session.add(employee)
#     session.commit()
#
# """
# This is for creating DB records and commit them to DB
# """
    """Adding multi records"""
    # data = [{"first_name":"Blayne","last_name":"Pickavance","age":1},
    # {"first_name":"Mattheus","last_name":"Oxbie","age":2},
    # {"first_name":"Pattin","last_name":"Keeping","age":3},
    # {"first_name":"Cindi","last_name":"Havercroft","age":4},
    # {"first_name":"Aguste","last_name":"Brosnan","age":5},
    # {"first_name":"Jourdain","last_name":"Baughn","age":6},
    # {"first_name":"Danny","last_name":"Donalson","age":7},
    # {"first_name":"Kaela","last_name":"Gronow","age":8},
    # {"first_name":"Lisa","last_name":"Bonnet","age":9},
    # {"first_name":"Retha","last_name":"Huchot","age":10},
    # {"first_name":"Lynsey","last_name":"Blannin","age":11},
    # {"first_name":"Angelle","last_name":"Huddlestone","age":12},
    # {"first_name":"Elbertine","last_name":"Hise","age":13},
    # {"first_name":"Timothee","last_name":"Dreinan","age":14},
    # {"first_name":"Rosana","last_name":"Drackford","age":15},
    # {"first_name":"Sherye","last_name":"McDirmid","age":16},
    # {"first_name":"Monica","last_name":"Spoole","age":17},
    # {"first_name":"Dominic","last_name":"Sorey","age":18},
    # {"first_name":"Carole","last_name":"Flipsen","age":19},
    # {"first_name":"Tommi","last_name":"Baccas","age":20},
    # {"first_name":"Aliza","last_name":"Jacklin","age":21},
    # {"first_name":"Hubie","last_name":"Graine","age":22},
    # {"first_name":"Sherye","last_name":"Dosdale","age":23},
    # {"first_name":"Shelley","last_name":"Klehn","age":24},
    # {"first_name":"Ellie","last_name":"Matton","age":25},
    # {"first_name":"Berny","last_name":"Boler","age":26},
    # {"first_name":"Mathias","last_name":"Straine","age":27},
    # {"first_name":"Rudy","last_name":"Coles","age":28},
    # {"first_name":"Grant","last_name":"Pargeter","age":29},
    # {"first_name":"Micah","last_name":"Sefton","age":30},
    # {"first_name":"Leon","last_name":"Whitington","age":31},
    # {"first_name":"Tobey","last_name":"Bruni","age":32},
    # {"first_name":"Martynne","last_name":"Searchwell","age":33},
    # {"first_name":"Ruben","last_name":"Dowsett","age":34},
    # {"first_name":"Maire","last_name":"McDade","age":35},
    # {"first_name":"Tobin","last_name":"Paddefield","age":36},
    # {"first_name":"Randolf","last_name":"Graith","age":37},
    # {"first_name":"Enriqueta","last_name":"Antonnikov","age":38},
    # {"first_name":"Vlad","last_name":"Steer","age":39},
    # {"first_name":"Buckie","last_name":"O' Connell","age":40},
    # {"first_name":"Hayes","last_name":"Pedgrift","age":41},
    # {"first_name":"Mady","last_name":"Thredder","age":42},
    # {"first_name":"Sisile","last_name":"O'Hartagan","age":43},
    # {"first_name":"Sherie","last_name":"Gimber","age":44},
    # {"first_name":"Jamison","last_name":"Poskitt","age":45},
    # {"first_name":"Keith","last_name":"Nuth","age":46},
    # {"first_name":"Glenden","last_name":"Hawksley","age":47},
    # {"first_name":"Merna","last_name":"Surmon","age":48},
    # {"first_name":"Aloysius","last_name":"Berringer","age":49},
    # {"first_name":"Karlens","last_name":"Dearnley","age":50},
    # {"first_name":"Ase","last_name":"Taudevin","age":51},
    # {"first_name":"Lavena","last_name":"Duffree","age":52},
    # {"first_name":"Hedvig","last_name":"Seivwright","age":53},
    # {"first_name":"Tabor","last_name":"Cabedo","age":54},
    # {"first_name":"Bernie","last_name":"Mains","age":55},
    # {"first_name":"Retha","last_name":"Raise","age":56},
    # {"first_name":"Cornela","last_name":"Belliveau","age":57},
    # {"first_name":"Peggie","last_name":"Quilkin","age":58},
    # {"first_name":"Kahaleel","last_name":"Wadforth","age":59},
    # {"first_name":"Anthony","last_name":"Persicke","age":60},
    # {"first_name":"Martina","last_name":"Etridge","age":61},
    # {"first_name":"Aristotle","last_name":"Springford","age":62},
    # {"first_name":"Nathaniel","last_name":"Bartelot","age":63},
    # {"first_name":"Nap","last_name":"Bediss","age":64},
    # {"first_name":"Kaia","last_name":"Copp","age":65},
    # {"first_name":"Araldo","last_name":"Joules","age":66},
    # {"first_name":"Derward","last_name":"Vanderson","age":67},
    # {"first_name":"Florance","last_name":"Barracks","age":68},
    # {"first_name":"Noel","last_name":"Kempson","age":69},
    # {"first_name":"Aluino","last_name":"Gaymar","age":70},
    # {"first_name":"Arch","last_name":"Clucas","age":71},
    # {"first_name":"Estella","last_name":"Twinterman","age":72},
    # {"first_name":"Pia","last_name":"Ackerman","age":73},
    # {"first_name":"Aile","last_name":"Poyle","age":74},
    # {"first_name":"Barron","last_name":"Roakes","age":75},
    # {"first_name":"Regina","last_name":"Branche","age":76},
    # {"first_name":"Paola","last_name":"Congram","age":77},
    # {"first_name":"L;urette","last_name":"Adamson","age":78},
    # {"first_name":"Fabio","last_name":"Willimot","age":79},
    # {"first_name":"Rochette","last_name":"Kobierski","age":80},
    # {"first_name":"Danyelle","last_name":"Parnham","age":81},
    # {"first_name":"Lorain","last_name":"Wybrew","age":82},
    # {"first_name":"Ganny","last_name":"Josovitz","age":83},
    # {"first_name":"Bonny","last_name":"Parham","age":84},
    # {"first_name":"Tammy","last_name":"Tanzig","age":85},
    # {"first_name":"Donelle","last_name":"Reany","age":86},
    # {"first_name":"Eugine","last_name":"Petracek","age":87},
    # {"first_name":"Christin","last_name":"Ramsden","age":88},
    # {"first_name":"Meir","last_name":"Shillinglaw","age":89},
    # {"first_name":"Eachelle","last_name":"Headey","age":90},
    # {"first_name":"Stanley","last_name":"Chancelier","age":91},
    # {"first_name":"Em","last_name":"MacVay","age":92},
    # {"first_name":"Rena","last_name":"Zohrer","age":93},
    # {"first_name":"Jody","last_name":"Drakeley","age":94},
    # {"first_name":"Stefanie","last_name":"Baly","age":95},
    # {"first_name":"Daune","last_name":"Corwin","age":96},
    # {"first_name":"Cariotta","last_name":"Cavnor","age":97},
    # {"first_name":"Leoline","last_name":"Sabater","age":98},
    # {"first_name":"Glad","last_name":"Maltster","age":99},
    # {"first_name":"Briana","last_name":"Gavey","age":100}]
    #
    # for d in data:
    #     employee = Employee(
    #         first_name=d['first_name'],
    #         last_name=d['last_name'],
    #         age=d['age']
    #     )
    #     session.add(employee)
    #
    # session.commit()

    """Taking data from DB"""
    # employees = session.query(Employee).all()
    # for e in employees:
    #     print(e.first_name, e.last_name, e.age)

    """Taking data using 'startswith' and filter using order_by and 'or'"""
    # employees = session.query(Employee).where(
    #     (Employee.first_name.startswith('M')) | (Employee.age > 60)
    # ).order_by(Employee.age.desc())
    # for e in employees:
    #     print(e.first_name, e.last_name, e.age)

    """Taking data and updating 'first_name'"""
    # employee = session.query(Employee).first()
    # employee.first_name = "Mikeeyh"
    # session.commit()
    # print(employee.first_name, employee.last_name)

    """Taking data and deleting by 'first_name'"""
    # employee = session.query(Employee).filter_by(first_name="Mikeeyh").first()
    # session.delete(employee)
    # session.commit()

    """Adding cities"""
    # session.add_all((
    #     City(name='Sofia'),
    #     City(name='Pernik'),
    #     City(name='Montana'),
    #     City(name='Vraca'),
    #     City(name='Vidin')
    # ))
    # session.commit()

    """Adding random city_id to each employee"""
    # employees = session.query(Employee).all()
    # for e in employees:
    #     e.city_id = random.randint(1, 5)
    # session.commit()

    """Taking all employees from specific city"""
    city = session.query(City).first()
    for e in city.employees:
        print(e.first_name, e.last_name, city.name)