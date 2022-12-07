CREATE DATABASE  IF NOT EXISTS `donaldsontwitter` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `donaldsontwitter`;
-- MySQL dump 10.13  Distrib 8.0.30, for Win64 (x86_64)
--
-- Host: donaldson-twitter-development.mysql.database.azure.com    Database: donaldsontwitter
-- ------------------------------------------------------
-- Server version	8.0.28

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `battelec`
--

DROP TABLE IF EXISTS `battelec`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `battelec` (
  `word` varchar(255) NOT NULL,
  UNIQUE KEY `word_UNIQUE` (`word`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `battelec`
--

LOCK TABLES `battelec` WRITE;
/*!40000 ALTER TABLE `battelec` DISABLE KEYS */;
INSERT INTO `battelec` VALUES ('%batteries%'),('%battery%'),('%electric%'),('%Lithium%'),('%volt%');
/*!40000 ALTER TABLE `battelec` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `handles`
--

DROP TABLE IF EXISTS `handles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `handles` (
  `id` bigint NOT NULL,
  `username` varchar(60) NOT NULL,
  `description` varchar(1024) DEFAULT NULL,
  `name` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `handles`
--

LOCK TABLES `handles` WRITE;
/*!40000 ALTER TABLE `handles` DISABLE KEYS */;
INSERT INTO `handles` VALUES (12637732,'DaimlerTruck','For all who keep the world moving.','Daimler Truck AG'),(15101714,'CaterpillarInc','We help our customers build a better, more sustainable world. #LetsDoTheWork','CaterpillarInc'),(15676492,'Ford','Helping to build a better world where every person is free to move and pursue their dreams.','Ford Motor Company'),(16080510,'vauxhall','Official Vauxhall Twitter. Share your photos using #MyVauxhall\nSee our privacy policy https://t.co/l6fAUHoPA5','Vauxhall'),(16144151,'renaultgroup','Home of innovative talents across the world. Builders of a sustainable future, we are pioneering mobility since 1898. ⚡','Renault Group'),(16529238,'subaru_usa','Official Twitter for Subaru of America. Scroll for some #SubieLove ?...','Subaru'),(17596020,'ScaniaGroup','The latest from Scania, leading supplier of sustainable transport solutions and services, engines for industrial and marine applications, and power generation.','Scania Group'),(18193132,'CrownEquipment','An official source of news and information from one of the world’s leading material handling companies. #MaterialHandling #CrownEquipment #CrownLiftTrucks','Crown Equipment'),(18238328,'VolvoGroup','We are committed to shaping the future landscape of sustainable transport and infrastructure solutions. Our shares are listed on Nasdaq in Stockholm, Sweden.','Volvo Group'),(18344399,'arcticcat_snow','Trouble makers. History makers. Check out our 2022 Snowmobile line up','Arctic Cat - Snow'),(18726666,'JohnDeere','Nothing runs like a Deere','John Deere'),(22047929,'GMcanada','Creating a world with #ZeroCrashes, #ZeroEmissions & #ZeroCongestion, right here in Canada. Join us: https://t.co/6Y4JxrJuRO Privacy Statement: https://t.co/EskDLUj7yh','GM Canada'),(22444611,'mitsucars','Official Twitter for Mitsubishi Motors USA  #DriveYourAmbition','Mitsubishi Motors USA'),(22834687,'ArcticCatORV','For decades, the name Arctic Cat has inspired adventurers everywhere. Now part of the Textron family, we deliver power, performance and precision engineering.','Arctic Cat Off Road'),(23587906,'RideCannondale','Come Ride With Us.','Cannondale'),(23650884,'freightliner','Freightliner Trucks is one of the most recognized and respected names in the industry. We offer trucks that are engineered to profit our customers.','Freightliner Trucks'),(23651888,'DemandDetroit','Leading the industry with our diesel engines, axles, transmissions, telematics & safety solutions. \n\nIf you demand the best, #DemandDetroit.','Detroit'),(23689478,'Kia','The official Twitter account of Kia America.','Kia America'),(25810212,'navistar','Welcome to the official Twitter Feed for Navistar, Inc.','Navistar'),(26007726,'Hyundai','Hi, we\'re Hyundai – pronounced like Sunday. Follow us for the latest news, vehicle reveals, and exclusive content. #ItsYourJourney. Start exploring.','Hyundai USA'),(28165910,'VW','Before it can change the world, it has to change yours ? Reserve your all-electric, zero-direct emissions #VWID4 today. https://t.co/x9MaRBKnWS','Volkswagen'),(29679737,'AudiOfficial','What\'s your story of progress? We are here to listen. Reach out to our Customer Care via https://t.co/hhSBCoe3Yw','Audi'),(32213881,'suzukicycles','Official Suzuki Motor USA, LLC Motorcycles, Scooters, and ATVs Twitter Account. Also on Facebook at: https://t.co/fQdFwLpdGy','Suzuki'),(33640141,'PeterbiltMotors','Peterbilt has reigned as America\'s premium truck manufacturer since the company’s founding in 1939 by providing best-in-class features and innovations.','Peterbilt Motors Co.'),(34300916,'KenworthTruckCo','Kenworth Truck Company is the manufacturer of        The World’s Best® heavy and medium duty trucks.','Kenworth Truck Co.'),(39825433,'CaseCE','CASE produces 15 lines of equipment and more than 90 models to meet your toughest construction challenges.','casece'),(40773994,'agralesa','A Agrale é uma empresa brasileira cada vez mais internacionalizada que ao longo dos anos conquistou respeito e admiração nos países em que está presente.','Agrale'),(41201893,'WstrnStarTrucks','Official Twitter of Western Star Trucks. Truck manufacturer producing a range of Class 8 commercial vehicles for both highway and off-road use.','WstrnStarTrucks'),(42665784,'SAICinc','Advancing the power of technology and innovation to serve and protect our world. #BringOnTomorrow','SAIC'),(43430484,'Honda','Official news & information from Honda\'s Social team at American Honda HQ in Torrance, Calif. For Customer Service ?\'s tweet @HondaCustSvc','Honda'),(45550539,'Stellantis','Stellantis is one of the world\'s leading automakers and a mobility provider: powered by our diversity, we lead the way the world moves.','Stellantis'),(58365266,'HINOTRUCKSUSA','When you make the decision to go Hino, you\'re not just getting a truck, you become part of a way of doing business that delivers to the bottom line.','Hino Trucks'),(58458203,'MANtruckandbus','Simplifying customer business through leading sustainable solutions. Driving responsible transport. Tweets in English & German.\n\nImprint: https://t.co/XQOPjDZki6','MAN Truck & Bus'),(63479512,'VolvoPentaNA','Volvo Penta of the Americas is a world-leading supplier of engines and complete power systems for marine and industrial applications.','Volvo Penta'),(71370472,'UDTrucks','The UD name means quality.','UD TRUCKS'),(75123376,'komatsuconstrna','Official Komatsu corporate account sharing construction product news, photos, videos, articles and more','Komatsu Construction North America'),(84405610,'RUMOAUTOPECAS','Desde 1991,Somos Especialista em Peças para Veículos Importados e Nacionais Central de atendimento ( 11 ) 3389-3253 / Seg. à Sex. 8hs às 19hs / sáb.8hs às 17hs','Rumo Auto-Peças'),(87299367,'Cummins','Trains powered by hydrogen. Earth movers powered by electricity. Big engines made efficient with big data. At Cummins, the future pulls us forward.','Cummins Inc.'),(88803528,'MazdaUSA','Welcome to the official Mazda USA Twitter account. Have a Mazda story? A question? Let us know.','Mazda USA'),(88898508,'IVECO','Iveco designs, manufactures, and markets a broad range of light, medium and heavy commercial vehicles, off-road trucks, city and intercity buses and coaches.','IVECO'),(93608485,'NissanMotor','Follow for official news, insights and exclusives from the owner of Nissan and INFINITI brands.','Nissan Motor'),(105187911,'vidhataindia','basant products india\nhttp://t.co/yxDPKL6Ena','Vishal garg'),(107122128,'BMWGroup','Welcome to the official #BMWGroup account. Imprint: https://t.co/V00v5c01kz Privacy Policy: https://t.co/fBbpTMVWRN…','BMW Group'),(108884409,'Tumosan','Tümosan Motor ve Traktör Sanayi A.Ş. 1976 yılından günümüze kadar motor ve traktör üretimi yapmaktadır.','Tümosan'),(109562416,'DoosanPortable','Dealer Locator: https://t.co/L0Vd85XpZB\n#morethanpower','DoosanPortablePower'),(124162005,'steyr_motors','','Steyr Motors'),(127613373,'FIATUSA','The official Twitter of FIAT USA. For Customer Care, please reach out to @fiatcares. For more: https://t.co/tKNOAJPN3z https://t.co/ZaGO1mn0rT','FIAT USA'),(140582641,'chevroletbrasil','#EncontreNovosCaminhos Saiba mais em: https://t.co/TZFBJJIuPr','Chevrolet Brasil'),(159508255,'NavistarNews','Welcome to the official news account of Navistar, a leading manufacturer of commercial trucks, buses and engines from brands @IntnlTrucks and IC Bus.','Navistar Newsroom'),(161673065,'DAFTrucksNV','Welcome to the global DAF #Trucks account for all fans of everything DAF related ?! https://t.co/XDbiJaI56Q & https://t.co/kgm6e7L8M0','DAF Trucks N.V.'),(166927629,'man_e_s','Tune in and interact with technology and news from MAN Energy Solutions, leading in advanced engineering across the marine, energy and industrial sectors.','MAN Energy Solutions'),(173777950,'UzelTraktor','http://t.co/DxGJu6c6Xk','Uzel Traktor'),(194341732,'ssangyongcol','Bienvenidos al mundo de las buenas decisiones. Somos representantes exclusivos de las SUVs que los colombianos prefieren. Twitter oficial de #SsangYong.','Ssangyong Motor Colombia'),(205782410,'StandardMotors','General Motors Chevrolet,Buick,GMC & Certified Pre-Owned vehicle dealership in Southwest Saskatchewan. GM Goodwrench Service,Parts Department,& Body Shop.','Standard Motors'),(224359740,'MercedesBenzUSA','Official page of Mercedes-Benz USA','Mercedes-Benz USAㅤ'),(237286205,'BriggsStratton','Briggs & Stratton, LLC is focused on providing power to get work done and make people\'s lives better.','Briggs & Stratton'),(267399199,'generalelectric','Every minute of every day, GE rises to the challenge of building a world that works.','General Electric'),(307826219,'MahindraRise','A tech & innovation-led global federation of companies that provides a range of products, services & possibilities, enabling people to #Rise. #TogetherWeRise','Mahindra Group'),(311908204,'ABCengine','ABC is manufacturing diesel engines since 1912. The company has the reputation of building robust  engines, with low fuel and oil consumption.','Anglo Belgian Corp.'),(337704468,'TatraTrucks','TATRA TRUCKS A.S. is one of the oldest vehicle manufacturers in the world.','TATRA TRUCKS'),(342772500,'volvocars','#ForEveryonesSafety','Volvo Cars'),(359851028,'TataMotorsNews','Follow us for latest updates on Tata Motors','Tata Motors News'),(364289910,'KOHLERPower','Welcome to the official KOHLER Generators page. Ask us questions, share your thoughts and keep up on the latest news.','KOHLER Power - Generators'),(364948131,'MackTrucks','Official Mack Trucks ?\n\n? | Get featured #MackTrucks + #MackTrucksMonday\n? | Send trucks and dogs #MyDogIsMyCopilot\n? | Learn more: https://t.co/UU5XUt6Zab','Mack Trucks'),(428544934,'navecofrance','Réservez votre #Chauffeur #Privé #VTC en avance depuis notre application.\nTéléchargez l\'application :\nhttps://t.co/knRQa2MThC…','NAVECO'),(436200322,'KIOTITractor','#WeDigDirt. KIOTI offers a full line of compact tractors, UTVs and ZTRs.','KIOTITractor'),(601176025,'PolarisInc','Polaris Inc. pioneers product breakthroughs and enriching experiences and services that have invited people to discover the joy of being outdoors since 1954.','Polaris Inc.'),(819722048,'JCBmachines','Always looking for a better way. The official JCB Twitter account.','JCB'),(822658698,'GAC_MOTOR','Welcome to the official #GACMOTOR account. EXCELLENT CAR FOR LOVED ONES!\nAfter-Sales Service Tel: 00864001589999','GAC MOTOR'),(865614979,'TATAMotorTrucks','Tata Motors is committed to maximizing customer satisfaction - http://t.co/z6FlzYIrXB','TATA Trucks SA'),(918864206,'basaktraktortr','https://t.co/K31ebpoer0\nhttps://t.co/6WJcTkTIQi','Başak Traktör'),(1036525171,'XCMGGroup','World\'s 3rd largest manufacturer of construction machinery with great excavators, loaders, cranes, rollers, graders and more.','XCMGGroup'),(1088062616,'Hyundai_Global','Welcome to the #Hyundai official Twitter account. Our vision is clear: Progress for Humanity','Hyundai Worldwide'),(1151062694,'FPTIndustrial','#FPTIndustrial is a brand of @IvecoGroup_ ,dedicated to the design,production and sale of powertrains for all applications.','FPT Industrial'),(1250075179,'YamahaMotorUSA','Official Twitter page: Life can have many exciting, memorable experiences. Creating opportunities for them is what Yamaha is all about.','YamahaMotorUSA'),(1429016798,'VM_PRIDE','We offer advice, tips and tricks, and reviews about the best cars for YOU.','Valley Motors'),(1487268643,'CNHIndustrial','World-class equipment and services company. We sustainably advance the noble work of agriculture and construction workers. (NYSE: CNHI / MI: CNHI)','CNH Industrial'),(1685353908,'ETBIndia','VE Commercial Vehicles Limited (VECV) is a joint venture between the Volvo Group and Eicher Motors Limited.','Eicher Trucks&Buses'),(1706159101,'HINOJapan','日野自動車株式会社の国内公式アカウントです。日野自動車のさまざまなニュースをお届けします。  ソーシャルメディア運用ポリシー：https://t.co/28WpMP0TsJ','日野自動車株式会社'),(1901628055,'HitachiGlobal','Hitachi is becoming a Climate Change Innovator?\n✉Inquiries: https://t.co/CRtfDPH5Zf　\n?Community Guidelines: https://t.co/3RTbgGukR4','Hitachi'),(2179523612,'Maruti_Corp','Maruti Suzuki India Limited estd 1982, a subsidiary of Suzuki Motor Corporation of Japan, is India\'s largest passenger car company.','Maruti Suzuki'),(2510215220,'ToyotaMotorCorp','Official tweets from #Toyota Motor Corporation. #StartYourImpossible \nOur privacy policy can be viewed here: https://t.co/NvgOepGhnf','Toyota Motor Corp.'),(2744678503,'dongfeng_trucks','One of China\'s leading truck brands. We will be at IAA Hannover 25th September - 2nd October 2014 - hall 17, stand A27. #IAAHannover','Dongfeng Trucks'),(2850137795,'AROpumps','We Make Success Flow. ARO is a leading global manufacturer of positive displacement pumps & systems. Founded in 1930, ARO is a premier brand of Ingersoll Rand.','ARO Fluid Management'),(2882827345,'zongshen1992','','Zongshen Power'),(3003844230,'HISUNUSA','We make more than just powersports vehicles, we make off-road experiences that will last a lifetime.','HISUN MOTORS USA'),(3070804169,'ForkliftKomatsu','Official Twitter of Komatsu Forklift North America','Komatsu Forklift North America'),(3075543525,'zetortractors','Our tractors are used by more than 1.3 million customers around the world.? But we don\'t stop and we keep going. Because your satisfaction is our real engine.','ZETOR TRACTORS a.s.'),(3088687297,'jacmotorsglobal','Official global Twitter account of JAC Motors. Follow us and stay up-to-date on the latest JAC news.','JAC Motors Global'),(3173938893,'Progress_Rail','Progress Rail, a @CaterpillarInc company, provides complete rolling stock and infrastructure solutions to global railroad customers.','Progress Rail'),(3278308237,'WeichaiPowerCo','Weichai Power is one of the major global players in the R&D, #manufacturing and sales of diesel #engines for different kind of applications.','Weichai Power'),(3340804877,'BRP_Rotax','We get your heart beating. Our engines form the heart of legendary products such as Ski-Doo and Lynx snowmobiles, karts, recreational aircraft and others.','BRP-Rotax'),(3728212392,'BharatBenz1','Welcome to the official Twitter page of BharatBenz Trucks & Buses - a brand committed to the transformation of the Indian CV Industry.','BharatBenz'),(3773511569,'CushmanVehicles','Since 1901, Cushman has risen to the challenge, manufacturing industrial and utility vehicles that are built to last.','Cushman Vehicles'),(4826591811,'fordotosan','Şirketimizin tüm kurumsal ve sosyal faaliyetlerini sosyal medya sayfalarımızdan takip edebilir, Ford Otosan dünyasına dahil olabilirsiniz!','Ford Otosan'),(717921576369295363,'vidhatagroup','Mfr. & Exp. of Generators, Pumpsets, Alternators, PTO Generators, Pumps','Vidhatagroup'),(717971245656977409,'GreavesCottonIN','Official Handle of Greaves Cotton Limited. #GreavesElectricMobility #GrowWithGreaves #MovingBillionsWithGreaves #IndiaRollWithoutPetrol #MoreToLife @ampere_ev','Greaves Cotton'),(788748740899311618,'ThomasBuiltBus','The official Twitter feed of #thomasbuiltbuses, the leading manufacturer of Type A, C and D school buses.','Thomas Built Buses'),(805826824987168768,'UralMotors','Russian motorbike with 2-wheel drive and bar (not used Chain) designed for war.','URAL'),(829947820354383872,'CheryAutoCo','Official account of Chery Automobile Company. Chery Auto brings innovation and connivence to everyone around the globe.','Chery International'),(831405064489099264,'HMGnewsroom','Official global Twitter account of Hyundai Motor Group. Get the latest news to discover future insight. “Connecting to the Future”','Hyundai Motor Group'),(871703027627044868,'cmdbeml','Bharat Earth Movers Limited now known as BEML is an Indian Public Sector Undertaking, with headquarters in Bangalore.','CMDBEML'),(894913471640358913,'ALIndiaOfficial','Welcome to the official twitter handle of Ashok Leyland - The second largest manufacturer of commercial vehicles in India','Ashok Leyland'),(895107313068945408,'FusoOfficial','@fusoofficial をタグして、＃ふそうトラック部　又は　＃ふそうバス部 で投稿してね！たまに公式アカウントで紹介されるかも！\n\nUse #fusofan & tag @fusoofficial in your posts for a chance to be featured!','Mitsubishi Fuso Truck and Bus Corporation'),(923449123247812608,'fawde2017','China #VehicleEngine, Generating Set Engine, Other Engine, Semi Trailer, Dump Truck Manufacturers and Suppliers','Fawde VehicleEngine'),(972207437762703360,'HatzAmerica','Hatz Diesel of North America, Inc. is the factory headquarters for all of North America.','Hatz Diesel of North America, Inc.'),(989453906009714690,'ForceMotorsFML','A vertically integrated automobile company with expertise in design, development and manufacture of a range of automotive components, aggregates & vehicles.','Force Motors Ltd.'),(1054068550586036229,'allnewlada','Ваз 2108 No Mercy Артёма Демихова \nСамый быстрый Ваз в мире! \nET - 8.809 сек. @ 269.36 км/ч! \nЧемпионский автомобиль SMP RDRC 2018','Carsportal LADA'),(1067830618078228480,'generaldynamics','Official account for the General Dynamics Corporation.\n\nNYSE: GD','General Dynamics Corporation'),(1085313224059310081,'motor_simpson','','Simpson Motor Company'),(1088050638045540353,'BmcOtomotivTR','BMC Otomotiv Sanayi ve Ticaret A.Ş\'nin resmi Twitter hesabıdır.','BMC Otomotiv'),(1148529339203543040,'AGCO_Power','AGCO Power kuuluu maailman johtaviin työkoneiden dieselmoottorivalmistajiin ja on osa maatalouskonevalmistaja AGCO-konsernia. #agcopower','AGCO Power'),(1232894160648065024,'bee_taiwan','Taiwan Golden Bee,\nPlay Different','台灣金蜂Taiwan Golden Bee'),(1233287179645771781,'GWMGlobal','GWM (Great Wall Motor) is a global intelligent company committed to developing new energy vehicle solutions to ensure every person’s life is full of innovation.','GreatWallMotor'),(1356268918197915649,'deutz_ag','The engine company._Imprint: https://t.co/VrrOea124vPrivacy Policy: https://t.co/NDlVrrErPy','DEUTZ AG'),(1501147215427153926,'IndofarmTractor','A Leading Manufacturer of Tractors & Cranes under The Brand - INDO FARM & INDO POWER respectively.','Indo Farm Equipment Limited'),(1560435712939663360,'DS_siliconmetal','Anyang Dingsheng Silicon Industry Co., Ltd., Henan Province, China','Anyang Dingsheng Silicon Industry Co., Ltd.');
/*!40000 ALTER TABLE `handles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hce`
--

DROP TABLE IF EXISTS `hce`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hce` (
  `word` varchar(255) NOT NULL,
  UNIQUE KEY `word_UNIQUE` (`word`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hce`
--

LOCK TABLES `hce` WRITE;
/*!40000 ALTER TABLE `hce` DISABLE KEYS */;
INSERT INTO `hce` VALUES ('%H2-ICE%'),('%hydrogen%combustion%'),('%hydrogen%combustion%engine%');
/*!40000 ALTER TABLE `hce` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hfuelcell`
--

DROP TABLE IF EXISTS `hfuelcell`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hfuelcell` (
  `word` varchar(255) NOT NULL,
  UNIQUE KEY `word_UNIQUE` (`word`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hfuelcell`
--

LOCK TABLES `hfuelcell` WRITE;
/*!40000 ALTER TABLE `hfuelcell` DISABLE KEYS */;
INSERT INTO `hfuelcell` VALUES ('%#fuelcell%'),('%fuel%cell%'),('%hydrogen%powered%');
/*!40000 ALTER TABLE `hfuelcell` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `natgas`
--

DROP TABLE IF EXISTS `natgas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `natgas` (
  `word` varchar(255) NOT NULL,
  UNIQUE KEY `word_UNIQUE` (`word`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `natgas`
--

LOCK TABLES `natgas` WRITE;
/*!40000 ALTER TABLE `natgas` DISABLE KEYS */;
INSERT INTO `natgas` VALUES ('% lng %'),('%#lng%'),('%natural%gas%'),('%natural%gas%engine%'),('%natural%gas%pipeline%'),('%steam%turbine%');
/*!40000 ALTER TABLE `natgas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `referenced_tweets`
--

DROP TABLE IF EXISTS `referenced_tweets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `referenced_tweets` (
  `id` bigint NOT NULL,
  `author_id` bigint NOT NULL,
  `text` varchar(2048) NOT NULL,
  `created_at` datetime NOT NULL,
  `lang` varchar(5) DEFAULT NULL,
  `conversation_id` bigint DEFAULT NULL,
  `in_reply_to_user_id` bigint DEFAULT NULL,
  `powertrain_set` set('battElec','hFuelCell','hCE','natGas','hydrogen') DEFAULT NULL,
  `VADERcompound` decimal(5,4) DEFAULT NULL,
  `VADERneg` decimal(5,4) DEFAULT NULL,
  `VADERneu` decimal(5,4) DEFAULT NULL,
  `VADERpos` decimal(5,4) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `replies`
--

DROP TABLE IF EXISTS `replies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `replies` (
  `id` bigint NOT NULL,
  `author_id` bigint NOT NULL,
  `text` varchar(2048) NOT NULL,
  `created_at` datetime NOT NULL,
  `lang` varchar(5) DEFAULT NULL,
  `conversation_id` bigint DEFAULT NULL,
  `powertrain_set` set('battElec','hFuelCell','hCE','natGas') DEFAULT NULL,
  `VADERcompound` decimal(5,4) DEFAULT NULL,
  `VADERneg` decimal(5,4) DEFAULT NULL,
  `VADERneu` decimal(5,4) DEFAULT NULL,
  `VADERpos` decimal(5,4) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `tweets_ibfk_1` (`author_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `replies`
--

LOCK TABLES `replies` WRITE;
/*!40000 ALTER TABLE `replies` DISABLE KEYS */;
/*!40000 ALTER TABLE `replies` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `retweets`
--

DROP TABLE IF EXISTS `retweets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `retweets` (
  `id` bigint NOT NULL,
  `author_id` bigint NOT NULL,
  `text` varchar(2048) NOT NULL,
  `created_at` datetime NOT NULL,
  `lang` varchar(5) DEFAULT NULL,
  `conversation_id` bigint DEFAULT NULL,
  `in_reply_to_user_id` bigint DEFAULT NULL,
  `powertrain_set` set('battElec','hFuelCell','hCE','natGas','hydrogen') DEFAULT NULL,
  `VADERcompound` decimal(5,4) DEFAULT NULL,
  `VADERneg` decimal(5,4) DEFAULT NULL,
  `VADERneu` decimal(5,4) DEFAULT NULL,
  `VADERpos` decimal(5,4) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `retweet_fk_author` (`author_id`),
  CONSTRAINT `retweet_fk_author` FOREIGN KEY (`author_id`) REFERENCES `handles` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `tempvader`
--

DROP TABLE IF EXISTS `tempvader`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tempvader` (
  `id` bigint NOT NULL,
  `nega` decimal(5,4) DEFAULT NULL,
  `neu` decimal(5,4) DEFAULT NULL,
  `pos` decimal(5,4) DEFAULT NULL,
  `compound` decimal(5,4) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tempvader`
--

LOCK TABLES `tempvader` WRITE;
/*!40000 ALTER TABLE `tempvader` DISABLE KEYS */;
/*!40000 ALTER TABLE `tempvader` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `test_table`
--

DROP TABLE IF EXISTS `test_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `test_table` (
  `id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `test_table`
--

LOCK TABLES `test_table` WRITE;
/*!40000 ALTER TABLE `test_table` DISABLE KEYS */;
/*!40000 ALTER TABLE `test_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tweet_relationships`
--

DROP TABLE IF EXISTS `tweet_relationships`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tweet_relationships` (
  `this_tweet` bigint NOT NULL,
  `refers_to` bigint NOT NULL,
  `reference_type` enum('retweeted','quoted','replied_to') NOT NULL,
  KEY `tweet_references_ibfk_1_idx` (`this_tweet`),
  KEY `tweet_references_ibfk_2_idx` (`refers_to`),
  CONSTRAINT `tweet_relationships_ibfk_1` FOREIGN KEY (`this_tweet`) REFERENCES `retweets` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;



--
-- Table structure for table `tweets`
--

DROP TABLE IF EXISTS `tweets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tweets` (
  `id` bigint NOT NULL,
  `author_id` bigint NOT NULL,
  `text` varchar(2048) NOT NULL,
  `created_at` datetime NOT NULL,
  `lang` varchar(5) DEFAULT NULL,
  `conversation_id` bigint DEFAULT NULL,
  `powertrain_set` set('battElec','hFuelCell','hCE','natGas','hydrogen') DEFAULT NULL,
  `VADERcompound` decimal(5,4) DEFAULT NULL,
  `VADERneg` decimal(5,4) DEFAULT NULL,
  `VADERneu` decimal(5,4) DEFAULT NULL,
  `VADERpos` decimal(5,4) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `tweets_ibfk_1` (`author_id`),
  CONSTRAINT `tweets_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `handles` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;



/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-12-06 19:44:59