#!/usr/bin/env ruby

city_names = [
    'Toronto, Ontario',
    'Ottawa-Gatineau, Ontario/Quebec',
    'Vancouver, British Columbia',
    'Montreal, Quebec',
    'Edmonton, Alberta',
    'Winnipeg, Manitoba',
    'Saskatoon, Saskatchewan',
    'Calgary, Alberta',
    'Quebec, Quebec',
    'Halifax, Nova Scotia',
    'St. John\'s, Newfoundland and Labrador',
    'Saint John, New Brunswick',
    'Yukon',
    'Northwest Territories',
    'Nunavut'
]

crime_types = [
    '"Total, all violations",Actual incidents',
    '"Total, all violations","Rate per 100,000 population"',
    'Total violent Criminal Code violations,Actual incidents',
    'Total violent Criminal Code violations,"Rate per 100,000 population"',
    'Homicide,Actual incidents',
    'Homicide,"Rate per 100,000 population"'
]

subs = [
  ['Toronto, Ontario', 'Toronto'],
  ['Ottawa-Gatineau, Ontario/Quebec', 'Ottawa'],
  ['Vancouver, British Columbia', 'Vancouver'],
  ['Montreal, Quebec', 'Montreal'],
  ['Edmonton, Alberta', 'Edmonton'],
  ['Winnipeg, Manitoba', 'Winnipeg'],
  ['Saskatoon, Saskatchewan', 'Saskatoon'],
  ['Calgary, Alberta', 'Calgary'],
  ['Quebec, Quebec', 'Quebec'],
  ['Halifax, Nova Scotia', 'Halifax'],
  ['St. John\'s, Newfoundland and Labrador', 'St. John\'s'],
  ['Saint John, New Brunswick', 'Saint John']
]

puts "year,city,type,sub_type,number"

File.open(ARGV[0], "r:ISO8859-1") { |file|
  file.each_line() { |line|
    begin
      catch :line do
        city_names.each { |city|
          if (line =~ /.*#{city}.*/)
            crime_types.each { |crime|
              if (line =~ /.*#{crime}.*/)
                subs.each{|sub_pair|
                  line = line.gsub(sub_pair[0], sub_pair[1])
                }
                puts line
                throw :line
              end
            }
          end
        }
      end
    rescue ArgumentError
      # do nothing
    end
  }
}