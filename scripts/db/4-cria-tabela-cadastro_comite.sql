delimiter $$

CREATE TABLE `cadastro_comite` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(500) DEFAULT NULL,
  `email` varchar(500) DEFAULT NULL,
  `telefone` varchar(500) DEFAULT NULL,
  `cidade` varchar(500) DEFAULT NULL,
  `creation_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8$$
