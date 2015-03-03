//
//  FavoriesList.m
//  mCare
//
//  Created by Bob Webster on 12/14/14.
//  Copyright (c) 2014 vca. All rights reserved.
//

#import "FavoritesList.h"

@interface FavoritesList()
@property (strong, nonatomic) NSMutableArray *favorites;

@end

@implementation FavoritesList

+ (instancetype) sharedFavoritesList {
    static FavoritesList *shared = nil;
    static dispatch_once_t onceToken;
    
    dispatch_once(&onceToken, ^{
                  shared = [[self alloc] init];
    });
    return shared;
}


- (instancetype) init {
    self = [super init];
    if (self) {
        NSUserDefaults *defaults = [NSUserDefaults standardUserDefaults];
        NSArray *storedFavorites = [defaults objectForKey:@"favorites"];
        if (storedFavorites) {
            self.favorites = [storedFavorites mutableCopy];
        } else {
              self.favorites = [NSMutableArray array];
        }
    }
    return self;
   }


- (void)addFavorites:(id)item {
    [_favorites insertObject:item atIndex:0];
    [self saveFavorites];
}

- (void) removeFavorites:(id)item {
    [_favorites removeObject:item];
    [self saveFavorites];
}

- (void) saveFavorites {
    NSUserDefaults *defaults = [NSUserDefaults standardUserDefaults];
    [defaults setObject:self.favorites forKey:@"favorites"];
    [defaults synchronize];
}

@end

