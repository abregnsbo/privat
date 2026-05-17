#!perl -w
######################################################################-*-Perl-*-
#                                                                              #
#                      Copyright (C) 2008 Axel B.                              #
#                              All Rights Reserved.                            #
#                                                                              #
################################################################################

# 2004-04-06 Modified to encompass " on all posts. Added many new 2003 posts.
# 2006-11-26 Tilpasset Skandiabanken CSV format.
# 2008-03-22 Renamed to csv_virum.pl and changed to analyze fixed expenditures
#            into groups used in the Google budget_2007_2008 spreadsheet.
# 2009-05-03 Some record match strings updated. Updated help text. Added -d
#            option.
# 2009-10-25 Moved to CVS 'abregnsb_wtools' library; refer to log file here.
# 2024-02-04 Moved to github wtools.


use strict;

my $hlp_text =
"Usage: csv_virum.pl [OPTION] [FILE] ...
Group the records contained in FILE, and output the fields
sorted in groups.
  
  -d GRP:DATE   Print record details for group GRP on DATE, e.g. -d mad:2009-04
  -h, --help    Print this help text and exit
  -m, --month   Show groups for each month
  -r VAL
  -r MIN:MAX    Show ungrouped items, if VAL is negative shows expenses numerically
                larger than VAL, if positive shows incomes larger than VAL.
                VAL = 0 shows all ungrouped items.
                MIN:MAX will show the ungrouped items with expenses in the range
                MIN to MAX (both values included).
  -v, --verbose Print debug. Use multiple times for more chat

FILE(s) must be CSV formatted similar to the Jyske Bank CSV export format,
using ',' as decimal separater

Examples:
  ./csv_virum.pl -m ~/My\\ Documents/regnskab_penge/loenkonto_2000_2010.csv
";

my $verbose = 0;
my $show_month = 0;
my $show_remain = 0;
my $show_remain_val = 0;
my $show_remain_max = 0;
my $detail_grp;
my $detail_date;

while ($_ = $ARGV[0], /^-/) {
  shift;
  last if /^--$/;
  if (/^-h/ || /^--help/) {print $hlp_text; exit }
  if (/^-v/ || /^--verbose/) {$verbose++};
  if (/^-m/ || /^--month/) {$show_month++};
  if (/^-r/) {
    $show_remain++;
    $ARGV[0] =~ /([-0-9.]+)(:([-0-9.]+))?/;
    die "Non numerical argument to -r : '$1'\n" if ! defined $1;
    $show_remain_val = $1;
    $show_remain_max = defined $2 ? $3 : $1*1e99;
    shift;
  };
  if (/^-d/) {
    $ARGV[0] =~ /(.*):(.*)/;
    die "Bad argument to -d : '$ARGV[0]'\n" if ! (defined $1 || defined $2);
    $detail_grp = $1;
    $detail_date = $2;
    shift;
  };
  last if ! defined($ARGV[0]);
}

my @postering = ();

#------------------------------------------------------------------
# read posteringer & store in array
#------------------------------------------------------------------
my $err_cnt = 0;
my $ln_cnt = 0;
while (<>) {
  $ln_cnt++;
  chomp;
  # Eik Bank format
  my ($date,$mon,$year,$text,$amount,$saldo);
  if ((($date,$mon,$year,$text,$amount,$saldo) = /^(\d{2})-(\d{2})-(\d{4});"?\s*([^;]+?)"?;([^;]*);([^;]*);.*$/) || # Eik Bank
      (($date,$mon,$year,$text,$amount,$saldo) = /^"(\d{2})\.(\d{2})\.(\d{4})";"";"\s*(.*?)";"";"(.*?)";"(.*?)";"";"/)) { # Jyske Bank 
    $amount =~ s/\.//g; $amount =~ y/,/./;
    $saldo =~ s/\.//g;  $saldo =~ y/,/./;
    print "$saldo\n" if $verbose > 2;
    push @postering,
      {date   => $date,
       month  => $mon,
       year   => $year,
       text   => $text,
       amount => $amount,
       saldo  => $saldo};
  } elsif ($ln_cnt == 1) {
    # skip header line
  } elsif (/^\s*$/) {
    print "Line $. empty\n" if $verbose;
  } else {
    $err_cnt++;
    print "Error at line $.:\n$_\n" if $verbose;
  }
}
if ($verbose) {
  print "Processed $. lines, recorded " . (@postering) . " lines\n";
}
if ($err_cnt > 0) {
  print "Error in $err_cnt out of $ln_cnt lines\n";
}

my $Opvarmning = "fyringsolie|olie|hovedstadsregionens naturgas";
my $Forsikring = "topdanmark forsikring|fair forsikring";
my $Akasse = "ingeni.rernes arbejdsl.sheds|ledelse og .konomi a-kas|a-kasse";
my $El = "dong";
my $SuperMarkeder = "supermarked|[^s][^a]netto|bageri|bryggervang super|" .
                    "irma|k[øØ]bmand|7-eleven|aldi|asiens minimarked|" .
                    "fakta|GASTRONOMIA ITALIA|bornholmerkonditor|".
                    "N[øØ]RREBRO FRUGT-GR|rusland nota|F[øØ]TEX|".
                    "LYNHJEMS|FDB ISO |superbest|".
                    "^madpenge|^mad[: ]|bilka|kolonial|kiosk|".
                    "minimar|hamlet lavpris|kvickly|slagter|7 eleven|".
                    "fiskemanden|bryggervangen supe|fiskehallen|bagerg.rden|".
                    "emmerys|hemkop helsingborg|urtehuset|polonus|".
                    ".sterlandsk thehus";
# junk-mads restaurenter
my $JunkMad = "taco house|campania-pizza|mcdonalds|zelis pizza|" .
              "LE QUATTRO STAGION|the taco shop|il mulino pizza|".
              "amore pizza|burger king|mcdonald's|sharwarma grill|".
              "cafegrillen|big mamma|salat/sandwich bar";
my $Vaegtafgift = "centralregiste?ret for motor|rigspolitichefen/v.gtafgift";
my $Benzin = "jet 11|shell|q8|hydro texaco|ok\.bet\.aut|".
             "metax\. aut\.|Benzin|jet |statoil| ok |uno.x";

# Udkommenteret til mere anale tider:
# at det sjove/overfladisk lystige: i-byen, dans, gode restaurenter, biograf
#my $AtLeve = "shawarma|palads teatret|tatoverede enke|pejsegaarden|" .
#             "parkens bowling|illums bager|CHICO.S CANTINA|" .
#             "cinemaxx|amokka|the moose|olsen banden cafe|" .
#             "cafe norden|hereford house|egoisten|thai esan 2 restau|".
#             "brasserie degas|matahari jaya rest|sticks's sushi|".
#             "indian taj restaur|park cafe|jorden rundt|playtime";
#my $IByen = "GR[øØ]NDAL CENTRET|FORUM K[øØ]BENHAVN|STATENS MUSEUM";
#my $Cafe = "RENE CAFE|BRAMDRUPDAM CAFE|O.MURPHYS IRISH|JOHN BULL PUB";
#my $Toej = "BILLING SKO|KGS NYTORV SKO|levi store|hennes & maur|h&m|h & m|".
#           "paw sko|zara|josephine sko|inwear|kaza|savona sko|mr\. harris|".
#           "companys|levi sto|vero moda";
#my $PersonligPleje = "matas|body shop|KELIAN|zik zaks";
#my $Restaurent = "CAFE OVEN VISSE|NAPOLI RESTAURANT|no 1 .rhusgade";
#my $Tidskrifter = "Ingeni.ren|SNU kontigent|DEN KATOLSKE KIRKE|economist";
#my $Bolig = "Kurvemageren|ilva lyngby|ide m.bler|ikea|bauhaus|bahne|inspiration|".
#            "hvidevarelager|elgiganten";
## alle former for transport, dog ikke bil
#my $Transp = "taxa|taxi|BALLERUP-V.R\.-HERL|ryvang bilen|dsb s-tog|".
#             "dsb virum|DSB SVANEM.LLEN|LYNGBY.HOLTE|EUROPCAR|".
#             "peters bike supply|radio-codan";
#my $Bil = "bildillen|jet 11|p-hus|shell|q8|hydro texaco|ok\.bet\.aut|".
#          "metax\. aut\.|Fair Forsikring|henrik larsen auto|".
#          "Benzin|^bil:|rigspolitichefen/v.gtafgift|jet |statoil| ok |phus ".
#          "herlev syn|uno.x";
## Ferier
#my $BoligRenovation = "silvan|harald nyborg|topvvs|partek evers|".
#                      "forex|jfog konto|johannes fog|c\.rasmussen |".
#                      "green-line|jydsk vindueskom|bolig:|lavprisvvs|vvs\.online|".
#                      "scandinova|beckmanns|sadolin|rabat-vvs|jernpladsen|lavpris vvs|".
#                      "brobizz|sterbro t.mmer|hus: ";

#------------------------------------------------------------------
# process posteringer
#------------------------------------------------------------------
my %PostOversigt;
my $val;
my ($Year, $YearMon, $TimeIndx, $dato, $MonPostsRef, $PostRef);
foreach $PostRef (@postering) {
  if ($show_month) {
    $TimeIndx = "$PostRef->{year}-$PostRef->{month}";
  } else {
    $TimeIndx = "$PostRef->{year}";
  }
  $_    = $PostRef->{text};
  $val  = $PostRef->{amount};
  $dato = $PostRef->{date};
  #print "$TimeIndx, $_\t$val\n";
  if (/realkredit danmark/i) {
    $PostOversigt{"realkredit"}->{$TimeIndx} += (-$val);
  } elsif (/lyngby-taarb.k kommune/i && ($val < -1600 && $val > -5000)) {
    $PostOversigt{"dagpleje"}->{$TimeIndx} += (-$val);
  } elsif (/lyngby-taarb.k kommune/i && $val < -5000) {
    $PostOversigt{"grundskyld_vand_affald"}->{$TimeIndx} += (-$val);
  } elsif (/$Opvarmning/i) {
    $PostOversigt{"opvarmning"}->{$TimeIndx} += (-$val);
  } elsif (/$Akasse/i) {
    $PostOversigt{"A-kasse"}->{$TimeIndx} += (-$val);
  } elsif (/$Vaegtafgift/i) {
    $PostOversigt{"vaegtafgift"}->{$TimeIndx} += (-$val);
  } elsif (/$El/i) {
    $PostOversigt{"el"}->{$TimeIndx} += (-$val);
  } elsif (/$Benzin/i && $val<-250 && $val>-900) {
    $PostOversigt{"benzin"}->{$TimeIndx} += (-$val);
    if (defined $detail_grp && $detail_grp =~ /benzin/i) {
      print "$TimeIndx, $_\t$val\n" if $TimeIndx =~ /$detail_date/;
    }
  } elsif (/$Forsikring/i) {
    $PostOversigt{"forsikring"}->{$TimeIndx} += (-$val);
  } elsif (/first fitness/i) {
    $PostOversigt{"fitness"}->{$TimeIndx} += (-$val);
  } elsif (/dr licens/i) {
    $PostOversigt{"licens"}->{$TimeIndx} += (-$val);
  } elsif ((/$SuperMarkeder|$JunkMad/i && $val>-2000) ||
           (/$Benzin/i && $val>-200)) {
    $PostOversigt{"mad"}->{$TimeIndx} += (-$val);
    if (defined $detail_grp && $detail_grp =~ /mad/i) {
      print "$TimeIndx, $_\t$val\n" if $TimeIndx =~ /$detail_date/;
    }
  } else {
    push @{$PostOversigt{"mangel_poster"}}, $PostRef;
  }
}

if ((! $show_remain) && (! defined $detail_grp)) {
  my ($MonSum, $PostNavn);
  foreach $PostNavn (sort keys %PostOversigt) {
    $MonPostsRef = $PostOversigt{$PostNavn};
    next if $PostNavn =~ "mangel_poster";
    foreach $YearMon (sort keys %{$MonPostsRef}) {
      $MonSum = $MonPostsRef->{$YearMon};
      print "$PostNavn, $YearMon, $MonSum\n";
    }
  }
}

if ($verbose || $show_remain) {
  if (exists $PostOversigt{"mangel_poster"}) {
    print scalar(@{$PostOversigt{"mangel_poster"}}) . " ikke genkendte poster\n";
  }
}
foreach $PostRef (@{$PostOversigt{"mangel_poster"}}) {
  $YearMon = "$PostRef->{year}-$PostRef->{month}";
  $_   = $PostRef->{text};
  $val = $PostRef->{amount};
  if ($verbose > 1 || $show_remain) {
    if ($show_remain_val == 0 || 
        ($show_remain_val<0 && ($val<=$show_remain_val && $val>=$show_remain_max)) ||
        ($show_remain_val>0 && ($val>=$show_remain_val && $val<=$show_remain_max))) {
      print "$YearMon, $_\t$val\n";
    }
  }
}


################################################################################
#                                                                              #
#  End of file.                                                                #
#                                                                              #
################################################################################
