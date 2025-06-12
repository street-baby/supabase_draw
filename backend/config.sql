-- 用户表
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(100) NOT NULL COMMENT '用户邮箱',
  `password_hash` varchar(128) DEFAULT NULL COMMENT '密码哈希',
  `username` varchar(50) DEFAULT NULL COMMENT '用户名',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `last_login` datetime DEFAULT NULL COMMENT '最后登录时间',
  `is_active` tinyint(1) NOT NULL DEFAULT '1' COMMENT '是否激活',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 用户生成的图像表
CREATE TABLE `generated_images` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL COMMENT '用户ID',
  `prompt` text NOT NULL COMMENT '提示词',
  `image_url` varchar(255) NOT NULL COMMENT '图像URL',
  `style` varchar(50) DEFAULT NULL COMMENT '风格',
  `ratio` varchar(10) DEFAULT NULL COMMENT '比例',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;