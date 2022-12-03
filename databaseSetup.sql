CREATE DATABASE  IF NOT EXISTS `donaldsontwitter` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `donaldsontwitter`;

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
  `powertrain_set` set('battElec','hFuelCell','hCE','natGas') DEFAULT NULL,
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
  `powertrain_set` set('battElec','hFuelCell','hCE','natGas') DEFAULT NULL,
  `VADERcompound` decimal(5,4) DEFAULT NULL,
  `VADERneg` decimal(5,4) DEFAULT NULL,
  `VADERneu` decimal(5,4) DEFAULT NULL,
  `VADERpos` decimal(5,4) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `retweet_fk_author` (`author_id`),
  CONSTRAINT `retweet_fk_author` FOREIGN KEY (`author_id`) REFERENCES `handles` (`id`)
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
  CONSTRAINT `tweet_relationships_ibfk_1` FOREIGN KEY (`this_tweet`) REFERENCES `retweets` (`id`)
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
  `powertrain_set` set('battElec','hFuelCell','hCE','natGas') DEFAULT NULL,
  `VADERcompound` decimal(5,4) DEFAULT NULL,
  `VADERneg` decimal(5,4) DEFAULT NULL,
  `VADERneu` decimal(5,4) DEFAULT NULL,
  `VADERpos` decimal(5,4) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `tweets_ibfk_1` (`author_id`),
  CONSTRAINT `tweets_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `handles` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;