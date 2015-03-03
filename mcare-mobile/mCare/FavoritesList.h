//
//  FavoriesList.h
//  mCare
//
//  Created by Bob Webster on 12/14/14.
//  Copyright (c) 2014 vca. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface FavoritesList : NSObject
+ (instancetype)sharedFavoritesList;
- (NSArray *)favorites;
-(void)addFavorites:(id)item;
-(void)removeFavorites:(id)item;

@end
