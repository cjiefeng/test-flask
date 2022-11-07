CREATE TABLE `item_tab` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `item` varchar(255) NOT NULL,
  `quantity` int(11) NOT NULL,
  PRIMARY KEY (`id`)
);

INSERT INTO `item_tab` values (null, 'apple', 10), (null, 'orange', 10), (null, 'axe', 10);
