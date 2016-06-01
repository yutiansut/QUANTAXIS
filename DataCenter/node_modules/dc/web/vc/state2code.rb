#!/usr/bin/env ruby

state_code_map = {
    'ALABAMA'=>'AL',
    'ALASKA'=>'AK',
    'ARIZONA'=>'AZ',
    'ARKANSAS'=>'AR',
    'CALIFORNIA'=>'CA',
    'COLORADO'=>'CO',
    'CONNECTICUT'=>'CT',
    'DELAWARE'=>'DE',
    'DISTRICT OF COLUMBIA'=>'DC',
    'FLORIDA'=>'FL',
    'GEORGIA'=>'GA',
    'HAWAII'=>'HI',
    'IDAHO'=>'ID',
    'ILLINOIS'=>'IL',
    'INDIANA'=>'IN',
    'IOWA'=>'IA',
    'KANSAS'=>'KS',
    'KENTUCKY'=>'KY',
    'LOUISIANA'=>'LA',
    'MAINE'=>'ME',
    'MARYLAND'=>'MD',
    'MASSACHUSETTS'=>'MA',
    'MICHIGAN'=>'MI',
    'MINNESOTA'=>'MN',
    'MISSISSIPPI'=>'MS',
    'MISSOURI'=>'MO',
    'MONTANA'=>'MT',
    'NEBRASKA'=>'NE',
    'NEVADA'=>'NV',
    'NEW HAMPSHIRE'=>'NH',
    'NEW JERSEY'=>'NJ',
    'NEW MEXICO'=>'NM',
    'NEW YORK'=>'NY',
    'NORTH CAROLINA'=>'NC',
    'NORTH DAKOTA'=>'ND',
    'OHIO'=>'OH',
    'OKLAHOMA'=>'OK',
    'OREGON'=>'OR',
    'PENNSYLVANIA'=>'PA',
    'RHODE ISLAND'=>'RI',
    'SOUTH CAROLINA'=>'SC',
    'SOUTH DAKOTA'=>'SD',
    'TENNESSEE'=>'TN',
    'TEXAS'=>'TX',
    'UTAH'=>'UT',
    'VERMONT'=>'VT',
    'VIRGINIA'=>'VA',
    'WASHINGTON'=>'WA',
    'WEST VIRGINIA'=>'WV',
    'WISCONSIN'=>'WI',
    'WYOMING'=>'WY',
    'AMERICAN SAMOA'=>'AS',
    'GUAM'=>'GU',
    'NORTHERN MARIANA ISLANDS'=>'MP',
    'PUERTO RICO'=>'PR',
    'VIRGIN ISLANDS'=>'VI'
}

File.open(ARGV[0], 'r') { |file|
  file.each_line { |line|
    new_line = line
    line =~ /"name":"([\w\s]+)"/
    if ($1)
      state_name = $1.upcase()
      state_code = state_code_map[state_name]
      new_line = line.sub(/"name":"#{$1}"/, %{"name":"#{state_code}"})
    end

    puts new_line
  }
}
