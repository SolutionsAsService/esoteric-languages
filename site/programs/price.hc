U0 Price(U8 *what="Bread",I64 cents=250)
{
  "%s costs $$$$%d.%02d\n",what,cents/100,cents%100;
}
Price;
Price(,99);
Price("Milk");
