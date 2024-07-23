function myMin
  input Real a;
  input Real b;
  output Real result;
algorithm
  if a < b then
    result := a;
  else
    result := b;
  end if;
end myMin;