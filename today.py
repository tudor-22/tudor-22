import datetime
from dateutil import relativedelta
from lxml import etree

BIRTHDAY = datetime.datetime(2004, 8, 22)


def format_plural(unit):
    return 's' if unit != 1 else ''


def daily_readme(birthday):
    """Returns the time since birth, e.g. 'XX years, XX months, XX days'"""
    diff = relativedelta.relativedelta(datetime.datetime.today(), birthday)
    return '{} {}, {} {}, {} {}{}'.format(
        diff.years, 'year' + format_plural(diff.years),
        diff.months, 'month' + format_plural(diff.months),
        diff.days, 'day' + format_plural(diff.days),
        ' 🎂' if (diff.months == 0 and diff.days == 0) else '')


def update_age(filename, age):
    tree = etree.parse(filename)
    root = tree.getroot()
    for el in root.iter():
        if el.get('id') == 'age_data':
            el.text = age
        elif el.get('id') == 'age_data_dots':
            el.text = ' ' + '.' * max(2, 50 - len(age)) + ' '
    tree.write(filename, encoding='utf-8', xml_declaration=True)


if __name__ == '__main__':
    age = daily_readme(BIRTHDAY)
    for f in ('dark_mode.svg', 'light_mode.svg'):
        update_age(f, age)
    print('Updated uptime:', age)
